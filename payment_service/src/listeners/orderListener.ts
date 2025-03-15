import redisClient, { connectRedis } from "../config/redis";
import { initializePaymentService } from "../services/paymentService";

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
          console.log(`Processing payment for order: ${order_id}`);

          // Call Paystack API
          const payment = await initializePaymentService(
            user_id,
            order_id,
            email,
            parseFloat(total_price)
          );

          if (payment.status) {
            await redisClient.xAdd("payment_stream", "*", {
              order_id,
              status: "success",
            });
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
