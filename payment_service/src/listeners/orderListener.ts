import redisClient, { connectRedis } from "../config/redis";
import { initializePayment } from "../config/paystack";
import { Payment } from "../config/database"

async function listenForOrders() {
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
          const { order_id, user_id, email, total_price } = message;
          const amount = parseFloat(total_price)
          const reference = `pay_${order_id}`
          console.log(`Processing payment for order: ${order_id}`);

          // Call Paystack API
          const payment = await initializePayment(
            user_id,
            order_id,
            email,
            amount
          );
          const transaction = await Payment.create({
                userId: user_id,
                orderId: order_id,
                amount: amount,
                reference: reference,
                status: "pending",
            });
          if (payment.status) {
            await redisClient.xAdd("payment_stream", "*", {
              order_id,
              status: "success",
            });
            console.log("Payment successful")
            transaction.update({status: "success"})
          }

          lastId = id;
        }
      }
    } catch (err) {
      console.error("Error processing order:", err);
    }
  }
}

listenForOrders();
