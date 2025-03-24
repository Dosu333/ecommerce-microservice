import { ValidationError } from "../errors/errors";
import { verifyAccountNumber, createTransferRecipient } from "../config/paystack";
import Wallet from "../models/Wallet";


export const getWalletBalanceService = async (userId: string) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
    throw new ValidationError("Wallet not found");
  }
  return wallet.balance ?? 0.00;
};

export const createWalletService = async (userId: string) => {
    const wallet = await Wallet.create({ userId });
    return wallet;
};

export const updateWalletService = async (userId: string, accountNumber: string, bankCode: string) => {
    const wallet = await Wallet.findOne({ where: { userId } });
    if (!wallet) {
        throw new ValidationError("Wallet not found");
    }

    const response = await verifyAccountNumber(accountNumber, bankCode);
    if (!response) {
        throw new ValidationError("Account verification failed");
    }

    const recipientResponse = await createTransferRecipient(accountNumber, bankCode, response.account_name);
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
}

export const debitWalletService = async (userId: string, amount: number) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
    throw new ValidationError("Wallet not found");
  }
  if (wallet && wallet.balance !== undefined) {
    wallet.balance -= amount;
  }
  await wallet.save();
  return wallet.balance;
};

