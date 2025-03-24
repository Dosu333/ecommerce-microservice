import { ValidationError } from "../errors/errors";
import {
  verifyAccountNumber,
  createTransferRecipient,
  transferToAccount,
} from "../config/paystack";
import { sequelize } from "../config/database";
import Wallet from "../models/Wallet";
import Payment from "../models/Payment";

const createPaymentTransaction = async (userId: string, amount: number) => {
    const payment = await Payment.create({
        userId,
        amount,
        status: "pending"
    });
    return payment;
}

const updatePaymentStatus = async (reference: string, status: string) => {
    const payment = await Payment.findOne({ where: { reference } }); 
    if (!payment) {
        throw new ValidationError("Payment not found");
    }
    payment.status = status;
    await payment.save();
    return payment;
}

export const getWalletBalanceService = async (userId: string) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
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
    throw new ValidationError("Wallet not found");
  }

  const response = await verifyAccountNumber(accountNumber, bankCode);
  if (!response) {
    throw new ValidationError("Account verification failed");
  }

  const recipientResponse = await createTransferRecipient(
    accountNumber,
    bankCode,
    response.account_name
  );
  if (!recipientResponse) {
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
    throw new ValidationError("Invalid amount");
  }
  const transaction = await sequelize.transaction();
  try {
    const wallet = await Wallet.findOne({
      where: { userId },
      lock: transaction.LOCK.UPDATE,
      transaction,
    });

    if (!wallet) throw new ValidationError("Wallet not found");

    const payment = await createPaymentTransaction(userId, amount);
    const balance = wallet.balance ?? 0;
    if (balance < amount) throw new ValidationError("Insufficient funds");
    if (!wallet.recipientCode)
      throw new ValidationError("Please update your wallet details");
    if (!payment.reference) throw new ValidationError("Payment reference not found");

    const response = await transferToAccount(wallet.recipientCode, amount, payment.reference);
    if (!response) throw new ValidationError("Transfer failed");
    wallet.balance = balance - amount;
    await wallet.save({ transaction });
    await transaction.commit();
    await updatePaymentStatus(payment.reference, "success");
    return wallet.balance;
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
};
