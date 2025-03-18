import { initializePayment } from "../config/paystack";
import Payment from "../models/Payment";

export const initializePaymentService = async (userId: string, orderId: string, email: string, amount: number) => {
  const response = initializePayment(userId, orderId, email, amount)
  return response;
};