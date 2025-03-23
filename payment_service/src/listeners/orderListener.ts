import redisClient, { connectRedis } from "../config/redis";
import { Escrow, Wallet, Payment, sequelize } from "../config/database";
import { refundTransaction } from "../config/paystack";

async function listenForOrderEvents() {
    await connectRedis();
    let lastId = "0";

    while (true) {
        try {
            const result = await redisClient.xRead(
                { key: "order_stream", id: lastId },
                { BLOCK: 5000, COUNT: 10 }
            );

            if (result) {
                for (const { id, message } of result[0].messages) {
                    const { event, order_id } = message;

                    if (event === "order_delivered") {
                        await releaseEscrow(order_id);
                    } else if (event === "order_cancelled") {
                        await refundEscrow(order_id);
                    }

                    lastId = id;
                }
            }
        } catch (err) {
            console.error("Error listening to order events:", err);
        }
    }
}

async function releaseEscrow(orderId: string) {
    const transaction = await sequelize.transaction();
    try {
        const escrow = await Escrow.findOne({ 
          where: { orderId, status: "pending" },
          lock: transaction.LOCK.UPDATE,
          transaction
         });
        if (!escrow) return console.log(`No pending escrow for order: ${orderId}`);

        const sellerWallet = await Wallet.findOne({ 
          where: { userId: escrow.vendorId },
          lock: transaction.LOCK.UPDATE,
          transaction
        });
        if (!sellerWallet) return console.log('No wallet found for user')

        if (sellerWallet.balance !== undefined && escrow.amount !== undefined) {
            sellerWallet.balance += escrow.amount;
            await sellerWallet.save({ transaction });
        } else {
            console.error("Error: sellerWallet balance or escrow amount is undefined");
            return;
        }

        escrow.status = "released";
        await escrow.save({ transaction });
        await transaction.commit();
        console.log(`Escrow released for order ${orderId}. Funds credited to seller.`);
    } catch (error) {
        console.error("Error releasing escrow:", error);
        await transaction.rollback();
    }
}

async function refundEscrow(orderId: string) {
    const transaction = await sequelize.transaction();
    try {
        const escrow = await Escrow.findOne({ 
          where: { orderId, status: "pending" },
          lock: transaction.LOCK.UPDATE,
          transaction
        });
        if (!escrow) return console.log(`No pending escrow for order: ${orderId}`);

        const payment = await Payment.findOne({ where: { orderId, status:"success" } })
        if (!payment) return console.log("Transaction for the payment of order not found")

        const reference = payment.reference || ""
        const refundResult = await refundTransaction(reference, payment.amount)

        if (!refundResult) {
          console.error(`Refund failed for order ${orderId}`);
          return;
        }

        escrow.status = "refunded";
        await escrow.save({ transaction });
        await transaction.commit();
        console.log(`Escrow refunded for order ${orderId}. Funds credited to buyer.`);
    } catch (error) {
      await transaction.rollback();
      console.error("Error refunding escrow:", error);
    }
}

listenForOrderEvents();
