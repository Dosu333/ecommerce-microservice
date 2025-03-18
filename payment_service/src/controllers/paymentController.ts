import { Request, Response, NextFunction } from "express";
import { AuthenticationError, ValidationError } from "../errors/errors";
import { AuthenticatedRequest } from "../middleware/authenticationMiddleware";
import { initializePaymentService } from "../services/paymentService";
import redisClient, { connectRedis } from "../config/redis";


export const handleWebhook = async (req: Request, res: Response) => {
  const event = req.body;
  const { reference, status, metadata } = event.data;
  await connectRedis();

  if (status === "success") {
      const { order_id } = metadata;

      // Notify the order service through Redis stream
      await redisClient.xAdd("payment_stream", "*", {
          order_id,
          status: "paid"
      });
  }

  res.sendStatus(200);
};


export const initializePaymentController = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    try{
        const user = req.user;
        if (!user) {
            throw new AuthenticationError("Invalid login. Please login again");
        };
        const { orderId, amount } = req.body;
        const paymentUrl =  await initializePaymentService(user.user_id, orderId, user.email, amount)
        res.status(201).json({status:201, paymentUrl: paymentUrl, message:"Payment successfully initiated"});
    } catch(error) {
        next(error);
    }
}