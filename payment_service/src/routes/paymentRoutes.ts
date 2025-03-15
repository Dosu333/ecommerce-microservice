import { Router } from "express";
import { handleWebhook } from "../controllers/paymentController";


const router = Router();

router.post('/webhook', handleWebhook)


export default router