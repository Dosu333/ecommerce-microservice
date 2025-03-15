import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "../config/dotenv.config";

export const initializePaymentService = async (userId: string, orderId: string, email: string, amount: number) => {
  const reference = `pay_${orderId}`
  const response = await axios.post(
    "https://api.paystack.co/transaction/initialize",
    {
      email,
      amount: amount * 100,
      reference: reference,
    },
    {
      headers: { Authorization: `Bearer ${PAYSTACK_SECRET}` },
    }
  );
  await Payment.create({
    userId,
    orderId,
    amount,
    reference,
    status: "pending",
  });
  return response.data;
};
