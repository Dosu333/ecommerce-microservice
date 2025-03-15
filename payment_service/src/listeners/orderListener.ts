import redisClient from "../config/redis";
import { initializePaymentService } from "../services/paymentService";

async function listenForOrders() {
  while (true) {
    const result = await redisClient.xRead(
      { key: "order_stream", id: ">" },
      { BLOCK: 5000 }
    );

    if (result) {
      const messages = result[0].messages;

      for (const message of messages) {
        const { order_id, user_id, email, total_price } = message.message;
        console.log(`Processing payment for order: ${order_id}`);

        // Call Paystack API
        const payment = await initializePaymentService(user_id, order_id, email, parseFloat(total_price));
        
        if (payment.status) {
          await redisClient.xAdd("payment_stream", "*", {
            order_id,
            status: "success",
          });
        }
      }
    }
  }
}

listenForOrders();
