/**
 * @swagger
 * /payment/webhook:
 *   post:
 *     summary: Webhook to receive payment status updates
 *     description: |
 *       This endpoint receives webhook events from the payment gateway (e.g., Paystack).
 *       On successful payment, it updates the payment status, creates an escrow record, and notifies the order service via Redis stream.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               event:
 *                 type: string
 *               data:
 *                 type: object
 *                 properties:
 *                   reference:
 *                     type: string
 *                     description: Unique payment reference from Paystack
 *                   status:
 *                     type: string
 *                     enum: [success, failed]
 *                     description: Status of the payment
 *                   metadata:
 *                     type: object
 *                     properties:
 *                       order_id:
 *                         type: string
 *                         description: The order ID related to the payment
 *     responses:
 *       200:
 *         description: Webhook handled successfully
 *       400:
 *         description: Invalid request payload
 */

/**
 * @swagger
 * /payment/initialize:
 *   post:
 *     summary: Initialize a new payment
 *     description: |
 *       Starts the payment process for a given order. Returns a URL for the user to complete the payment.
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - orderId
 *               - vendorId
 *               - amount
 *             properties:
 *               orderId:
 *                 type: string
 *                 description: Unique identifier for the order
 *               vendorId:
 *                 type: string
 *                 description: Unique identifier for the vendor
 *               amount:
 *                 type: number
 *                 description: Amount to be paid in Naira (as an integer)
 *     responses:
 *       201:
 *         description: Payment initialized successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: number
 *                   example: 201
 *                 message:
 *                   type: string
 *                   example: Payment successfully initiated
 *                 data:
 *                   type: object
 *                   properties:
 *                     paymentUrl:
 *                       type: string
 *                       example: https://paystack.com/pay/abc123xyz
 *       400:
 *         description: Order has already been paid or invalid request
 *       401:
 *         description: Unauthorized request (invalid or missing token)
 */

/**
 * @swagger
 * /payment/transactions:
 *   get:
 *     summary: Retrieve all transactions for the logged-in user
 *     description: |
 *       Returns a list of all payment transactions (both successful and failed) made by the authenticated user.
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Transactions retrieved successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: number
 *                   example: 200
 *                 message:
 *                   type: string
 *                   example: Transactions retrieved successfully
 *                 data:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                       userId:
 *                         type: string
 *                       vendorId:
 *                         type: string
 *                       orderId:
 *                         type: string
 *                       amount:
 *                         type: number
 *                       status:
 *                         type: string
 *                         enum: [pending, success, failed]
 *                       reference:
 *                         type: string
 *                       createdAt:
 *                         type: string
 *                         format: date-time
 *       401:
 *         description: Unauthorized request (invalid or missing token)
 */

const paymentDocs = {};
export default paymentDocs;