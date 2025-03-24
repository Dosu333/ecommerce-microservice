import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import {
  createWalletController,
  getWalletBalanceController,
  updateWalletController,
  debitWalletController,
} from "../controllers/walletController";

const router = Router();

router.post("/create", createWalletController);
router.get("/balance", authenticateUser, getWalletBalanceController);
router.patch("/update", authenticateUser, updateWalletController);
router.post("/debit", authenticateUser, debitWalletController);

export default router;
