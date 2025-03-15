import { Request, Response, NextFunction } from "express";
import { AuthenticationError, ValidationError } from "../errors/errors";
import { AuthenticatedRequest } from "../middleware/authenticationMiddleware";
import { initializePaymentService } from "../services/paymentService";
import redisClient from "../config/redis";


export const handleWebhook = async (req: Request, res: Response) => {
  const { event, data } = req.body;

  if (event === "charge.success") {
    const orderId = data.reference.split("_")[1];

    // Store in Redis Stream for order service to process
    await redisClient.xAdd(
      "payment_stream",
      "*",
      { order_id: orderId, status: "success" }
    );
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