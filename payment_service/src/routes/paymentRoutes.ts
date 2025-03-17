import { Router } from "express";
import { authenticateUser } from "../middleware/authenticationMiddleware";
import { handleWebhook, initializePaymentController } from "../controllers/paymentController";


const router = Router();

router.post('/webhook', handleWebhook)
router.post('/initialize', authenticateUser, initializePaymentController)


export default router