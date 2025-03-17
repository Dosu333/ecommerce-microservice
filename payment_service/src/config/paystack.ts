import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "./dotenv.config";

export const initializePayment = async (userId: string, orderId: string, email: string, amount: number) => {
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
  return response.data;
};