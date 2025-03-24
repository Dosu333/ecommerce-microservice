import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import { createWalletController, getWalletBalanceController, updateWalletController } from "../controllers/walletController";


const router = Router();

router.post('/create', createWalletController)
router.get('/balance', authenticateUser, getWalletBalanceController)
router.patch('/update', authenticateUser, updateWalletController)


export default router