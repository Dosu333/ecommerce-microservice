import { Request, Response, NextFunction } from "express";
import { AuthenticationError, ValidationError } from "../errors/errors";
import { AuthenticatedRequest } from "../middleware/authenticationMiddleware";
import { getWalletBalanceService, createWalletService, debitWalletService } from "../services/walletService";
import { getEscrowBalanceService } from "../services/escrowService";

export const getWalletBalanceController = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    try {
        const user = req.user;
        if (!user) {
            throw new AuthenticationError("Invalid login. Please login again");
        }

        const [walletBalance, escrowBalance] = await Promise.all([
            getWalletBalanceService(user.user_id),
            getEscrowBalanceService(user.user_id)
        ]);

        const formatBalance = (balance: number) => 
            new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(balance ?? 0);

        res.status(200).json({ 
            status: 200, 
            data: { 
                walletBalance: formatBalance(walletBalance), 
                escrowBalance: formatBalance(escrowBalance) 
            }, 
            message: "Wallet balance retrieved successfully" 
        });
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