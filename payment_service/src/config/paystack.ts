import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "./dotenv.config";

export const initializePayment = async (userId: string, orderId: string, email: string, amount: number) => {
    const payment = await Payment.create({
        userId: userId,
        orderId: orderId,
        amount: amount,
        status: "pending",
      });

  const response = await axios.post(
    "https://api.paystack.co/transaction/initialize",
    {
      email,
      amount: amount * 100,
      reference: payment.reference,
      metadata: {
        user_id: userId,
        order_id: orderId
      },
    },
    {
      headers: { Authorization: `Bearer ${PAYSTACK_SECRET}` },
    }
  );
  return response.data.data.authorization_url;
};