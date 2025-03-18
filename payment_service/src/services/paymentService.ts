import { initializePayment } from "../config/paystack";
import Payment from "../models/Payment";

export const initializePaymentService = async (userId: string, orderId: string, email: string, amount: number) => {
  const reference = `pay_${orderId}`
  console.log("logging payment service")
  console.log(userId, orderId, email, amount, reference)
  const response = initializePayment(userId, orderId, email, amount)
  const payment = await Payment.create({
    userId: userId,
    orderId: orderId,
    amount: amount,
    reference: reference,
    status: "pending",
  });
  return response;
};