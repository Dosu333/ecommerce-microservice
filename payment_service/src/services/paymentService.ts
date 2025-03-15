import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "../config/dotenv.config";

export const initiatePaymentService = async (
  userId: string,
  orderId: string,
  amount: number,
  email: string
) => {
  const reference = `pay_${Date.now()}`;
  const paystackUrl = "https://api.paystack.co/transaction/initialize";

  const response = await axios.post(
    paystackUrl,
    { email, amount: amount * 100, reference },
    { headers: { Authorization: `Bearer ${PAYSTACK_SECRET}` } }
  );

  await Payment.create({
    userId,
    orderId,
    amount,
    reference,
    status: "pending",
  });

  return response.data.data.authorization_url;
};
