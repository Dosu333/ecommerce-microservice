import axios from "axios";
import Payment from "../models/Payment";
import logger from "./logger";
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
            logger.error("Account verification failed:", response.data.message);
            return null;
        }
    } catch (error) {
        logger.error("Error verifying account:", error);
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
            logger.info("Transfer Recipient Created:", response.data.data);
            return response.data.data;
        } else {
            logger.error("Failed to create recipient:", response.data.message);
            return null;
        }
    } catch (error) {
        logger.error("Error creating transfer recipient:", error);
        return null;
    }
};


export const transferToAccount = async (recipientCode: string, amount: number, reference: string) => {
    try {
        const response = await axios.post(
            "https://api.paystack.co/transfer",
            {
                source: "balance",
                amount: amount * 100, // Convert to kobo
                recipient: recipientCode,
                reference: reference,
            },
            {
                headers: {
                    Authorization: `Bearer ${PAYSTACK_SECRET}`,
                    "Content-Type": "application/json",
                },
            }
        );

        if (response.data.status) {
            logger.info("Transfer Successful:", response.data.data);
            return response.data.data;
        } else {
            logger.error("Transfer Failed:", response.data.message);
            return null;
        }
    } catch (error) {
        logger.error("Error processing transfer:", error);
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
            logger.info("Refund Successful:", response.data.data);
            return response.data.data;
        } else {
            logger.error("Refund Failed:", response.data.message);
            return null;
        }
    } catch (error) {
        logger.error("Error while processing refund:", error);
        return null;
    }
}
