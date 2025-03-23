import { Request, Response, NextFunction } from "express";
import { AuthenticationError, ValidationError } from "../errors/errors";
import { AuthenticatedRequest } from "../middleware/authenticationMiddleware";
import { getWalletBalanceService, createWalletService, debitWalletService } from "../services/walletService";

export const getWalletBalanceController = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  try {
    const user = req.user;
    if (!user) {
      throw new AuthenticationError("Invalid login. Please login again");
    }
    const balance = await getWalletBalanceService(user.user_id);
    res.status(200).json({ status: 200, data: { balance }, message: "Wallet balance retrieved successfully" });
  } catch (error) {
    next(error);
  }
};

export const createWalletController = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { vendorId } = req.body;
    const wallet = await createWalletService(vendorId);
    res.status(201).json({ status: 201, message: "Wallet created successfully" });
  } catch (error) {
    next(error);
  }
};