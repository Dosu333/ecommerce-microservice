import { ValidationError } from "../errors/errors";
import Wallet from "../models/Wallet";


export const getWalletBalanceService = async (userId: string) => {
  const wallet = await Wallet.findOne({ where: { userId } });
  if (!wallet) {
    throw new ValidationError("Wallet not found");
  }
  return wallet.balance;
};

export const createWalletService = async (userId: string) => {
    const wallet = await Wallet.create({ userId });
    return wallet;
};

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

