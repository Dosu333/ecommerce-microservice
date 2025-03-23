import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "./dotenv.config";

export const initializePayment = async (userId: string, vendorId: string, orderId: string, email: string, amount: number) => {
    const payment = await Payment.create({
        userId: userId,
        vendorId: vendorId,
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


export const refundTransaction = async (reference: string, amount: number | null) => {
    try {
        const response = await axios.post(
            "https://api.paystack.co/refund",
            {
                transaction: reference,
                amount: amount ? amount * 100 : undefined
            },
            {
                headers: {
                    Authorization: `Bearer ${PAYSTACK_SECRET}`,
                    "Content-Type": "application/json",
                },
            }
        );

        if (response.data.status) {
            console.log("Refund Successful:", response.data.data);
            return response.data.data;
        } else {
            console.log("Refund Failed:", response.data.message);
            return null;
        }
    } catch (error) {
        console.error("Error while processing refund:", error);
        return null;
    }
}
