/**
 * @swagger
 * /wallet/create:
 *   post:
 *     summary: Create a wallet for the vendor
 *     description: This endpoint allows a vendor to create a wallet. It requires the vendorId in the request body.
 *     tags:
 *       - Wallet
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               vendorId:
 *                 type: string
 *                 description: The ID of the vendor to create a wallet for.
 *                 example: "vendor123"
 *     responses:
 *       201:
 *         description: Wallet created successfully
 *       400:
 *         description: Bad Request (Invalid vendor ID or other issues)
 *       500:
 *         description: Internal Server Error
 */

/**
 * @swagger
 * /wallet/balance:
 *   get:
 *     summary: Get the wallet balance and escrow balance of the authenticated user
 *     description: This endpoint returns the wallet and escrow balances of the currently authenticated user.
 *     tags:
 *       - Wallet
 *     security:
 *       - BearerAuth: []
 *     responses:
 *       200:
 *         description: Successfully retrieved wallet and escrow balances
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: integer
 *                   example: 200
 *                 message:
 *                   type: string
 *                   example: Wallet balance retrieved successfully
 *                 data:
 *                   type: object
 *                   properties:
 *                     walletBalance:
 *                       type: string
 *                       example: "500.00"
 *                     escrowBalance:
 *                       type: string
 *                       example: "100.00"
 *       401:
 *         description: Unauthorized (No valid token or session)
 *       500:
 *         description: Internal Server Error
 */

/**
 * @swagger
 * /wallet/update:
 *   patch:
 *     summary: Update wallet details for the authenticated user
 *     description: This endpoint allows the authenticated user to update their wallet details (account number and bank code).
 *     tags:
 *       - Wallet
 *     security:
 *       - BearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               accountNumber:
 *                 type: string
 *                 description: The user's account number.
 *                 example: "1234567890"
 *               bankCode:
 *                 type: string
 *                 description: The user's bank code.
 *                 example: "044"
 *     responses:
 *       200:
 *         description: Wallet updated successfully
 *       400:
 *         description: Invalid account number or bank code
 *       401:
 *         description: Unauthorized (No valid token or session)
 *       500:
 *         description: Internal Server Error
 */

/**
 * @swagger
 * /wallet/debit:
 *   post:
 *     summary: Debit the wallet of the authenticated user
 *     description: This endpoint debits a specific amount from the user's wallet. The user must have sufficient balance to proceed with the debit.
 *     tags:
 *       - Wallet
 *     security:
 *       - BearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               amount:
 *                 type: number
 *                 description: The amount to debit from the wallet.
 *                 example: 50.00
 *     responses:
 *       200:
 *         description: Wallet debited successfully
 *       400:
 *         description: Invalid amount or insufficient funds
 *       401:
 *         description: Unauthorized (No valid token or session)
 *       500:
 *         description: Internal Server Error
 */

const walletDocs = {};
export default walletDocs;