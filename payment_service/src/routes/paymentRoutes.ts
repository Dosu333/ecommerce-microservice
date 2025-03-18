import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import { handleWebhook, initializePaymentController, getUserTransactionsController } from "../controllers/paymentController";


const router = Router();

router.post('/webhook', handleWebhook)
router.post('/initialize', authenticateUser, initializePaymentController)
router.get('/transactions', authenticateUser, getUserTransactionsController)


export default router