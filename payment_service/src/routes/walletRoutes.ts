import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import { createWalletController } from "../controllers/walletController";


const router = Router();

router.post('/create', createWalletController)


export default router