import { ValidationError } from "../errors/errors";
import {
  verifyAccountNumber,
  createTransferRecipient,
  transferToAccount,
} from "../config/paystack";
import { sequelize } from "../config/database";
import logger from "../config/logger";
import Wallet from "../models/Wallet";
import Payment from "../models/Payment";
import { log } from "console";

const createPaymentTransaction = async (userId: string, amount: number) => {
    const payment = await Payment.create({
        userId,
        amount,
        status: "pending"
    });
    return payment;
}

const updatePaymentStatus = async (payment: Payment, status: string) => {
    payment.status = status;
    await payment.save();
    return payment;
}

export const getWalletBalanceService = async (userId: string) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
    logger.error("Wallet not found");
    throw new ValidationError("Wallet not found");
  }
  return wallet.balance ?? 0.0;
};

export const createWalletService = async (userId: string) => {
  const wallet = await Wallet.create({ userId });
  return wallet;
};

export const updateWalletService = async (
  userId: string,
  accountNumber: string,
  bankCode: string
) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
    logger.error("Wallet not found");
    throw new ValidationError("Wallet not found");
  }

  const response = await verifyAccountNumber(accountNumber, bankCode);
  if (!response) {
    logger.error("Account verification failed");
    throw new ValidationError("Account verification failed");
  }

  const recipientResponse = await createTransferRecipient(
    accountNumber,
    bankCode,
    response.account_name
  );
  if (!recipientResponse) {
    logger.error("Recipient creation failed");
    throw new ValidationError("Recipient creation failed");
  }

  wallet.accountNumber = accountNumber;
  wallet.bankCode = bankCode;
  wallet.accountName = response.account_name;
  wallet.recipientCode = recipientResponse.recipient_code;
  wallet.bankName = recipientResponse.details.bank_name;
  await wallet.save();
  return wallet;
};

export const debitWalletService = async (userId: string, amount: number) => {
  if (amount <= 0) {
    logger.error("Invalid amount");
    throw new ValidationError("Invalid amount");
  }
  const transaction = await sequelize.transaction();
  try {
    const wallet = await Wallet.findOne({
      where: { userId },
      lock: transaction.LOCK.UPDATE,
      transaction,
    });

    if (!wallet) {
        logger.error("Wallet not found");
        throw new ValidationError("Wallet not found");
    };

    if (!wallet.recipientCode)
        throw new ValidationError("Please update your wallet details");

    const payment = await createPaymentTransaction(userId, amount);
    const balance = wallet.balance ?? 0;
    if (balance < amount) {
        await updatePaymentStatus(payment, "failed");
        logger.error(`Insufficient funds in wallet. Balance: ${balance}, Amount: ${amount}, User: ${userId}`);
        throw new ValidationError("Insufficient funds");
    };
    if (!payment.reference) throw new ValidationError("Payment reference not found");

    const response = await transferToAccount(wallet.recipientCode, amount, payment.reference);
    if (!response) {
        logger.error(`Transfer failed for user: ${userId}, reference: ${payment.reference}`);
        throw new ValidationError("Transfer failed");
    }
    wallet.balance = balance - amount;
    await wallet.save({ transaction });
    await transaction.commit();
    await updatePaymentStatus(payment, "success");
    return wallet.balance;
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
};
