import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import { createWalletController, getWalletBalanceController } from "../controllers/walletController";


const router = Router();

router.post('/create', createWalletController)
router.get('/balance', authenticateUser, getWalletBalanceController)


export default router