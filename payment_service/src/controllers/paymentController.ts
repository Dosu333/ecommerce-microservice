import { Request, Response, NextFunction } from "express";
import { AuthenticationError, ValidationError } from "../errors/errors";
import { AuthenticatedRequest } from "../middleware/authenticationMiddleware";
import { initializePaymentService, getUserTransactionsService } from "../services/paymentService";
import { Payment } from "../config/database"
import redisClient, { connectRedis } from "../config/redis";


export const handleWebhook = async (req: Request, res: Response) => {
  const event = req.body;
  const { reference, status, metadata } = event.data;
  const payment = await Payment.findOne({ where: { reference: reference } });
  await connectRedis();

  if (status === "success") {
    const { order_id } = metadata;

    // Notify the order service through Redis stream
    await redisClient.xAdd("payment_stream", "*", {
        order_id,
        status: "paid"
    });
    if (payment) {
      payment.update({status: "success"})
    }
  } else {
    if (payment) {
      payment.update({status: "failed"})
    }
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
        res.status(201).json({status:201, data: {paymentUrl}, message:"Payment successfully initiated"});
    } catch(error) {
        next(error);
    }
}

export const getUserTransactionsController = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  try {
    const user = req.user;
    if(!user) {
      throw new AuthenticationError("Invalid login. Please login again");
    }
    const payments = await getUserTransactionsService(user.user_id)
    res.status(200).json({status: 200, message: "Transactions retrieved successfully", data: payments})
  } catch(error) {
    next(error)
  }
}