import axios from "axios";
import Payment from "../models/Payment";
import { PAYSTACK_SECRET } from "./dotenv.config";

const paystackUrl = "https://api.paystack.co";

export const initializePayment = async (userId: string, vendorId: string, orderId: string, email: string, amount: number) => {
    const payment = await Payment.create({
        userId: userId,
        vendorId: vendorId,
        orderId: orderId,
        amount: amount,
        status: "pending",
      });

  const response = await axios.post(
    `${paystackUrl}/transaction/initialize`,
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


export const verifyAccountNumber = async (accountNumber: string, bankCode: string) => {
    try {
        const response = await axios.get(
            `${paystackUrl}/bank/resolve?account_number=${accountNumber}&bank_code=${bankCode}`,
            {
                headers: { Authorization: `Bearer ${PAYSTACK_SECRET}` },
            }
        );

        if (response.data.status) {
            return response.data.data;
        } else {
            console.log("Account verification failed:", response.data.message);
            return null;
        }
    } catch (error) {
        console.error("Error verifying account:", error);
        return null;
    }
};


export const createTransferRecipient = async (accountNumber: string, bankCode: string, name: string) => {
    try {
        const response = await axios.post(
            `${paystackUrl}/transferrecipient`,
            {
                type: "nuban",
                name,
                account_number: accountNumber,
                bank_code: bankCode,
                currency: "NGN"
            },
            {
                headers: {
                    Authorization: `Bearer ${PAYSTACK_SECRET}`,
                    "Content-Type": "application/json",
                },
            }
        );

        if (response.data.status) {
            console.log("Transfer Recipient Created:", response.data.data);
            return response.data.data;
        } else {
            console.log("Failed to create recipient:", response.data.message);
            return null;
        }
    } catch (error) {
        console.error("Error creating transfer recipient:", error);
        return null;
    }
};


export const refundTransaction = async (reference: string, amount: number | null) => {
    try {
        const response = await axios.post(
            `${paystackUrl}/refund`,
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
