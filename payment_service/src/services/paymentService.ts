import { ValidationError } from "../errors/errors";
import { initializePayment } from "../config/paystack";
import Payment from "../models/Payment";

export const initializePaymentService = async (userId: string, vendorId: string, orderId: string, email: string, amount: number) => {
  const existingPayment = await Payment.findOne({ where: { orderId, status:"success" } })
  if (existingPayment) {
    throw new ValidationError("Order has been paid for successfully")
  }
  const response = initializePayment(userId, vendorId, orderId, email, amount)
  return response;
};

export const getUserTransactionsService = async (userId: string) => {
  const payments = await Payment.findAll({ where: { userId } })
  return payments
}