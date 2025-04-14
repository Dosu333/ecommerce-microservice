# Payment Service 💳

## Overview 🌟

The **Payment Service** is a crucial component of our eCommerce platform. It manages payment processing, wallet operations, and handles updates from external providers like Paystack. This service ensures secure and seamless transactions between users and vendors, enabling purchases and wallet management.

---

## Table of Contents 📚

- [📦 Prerequisites](#prerequisites)
- [⚙️ Installation](#installation)
- [🔑 Environment Variables](#environment-variables)
- [🔌 Endpoints](#endpoints)
- [🛡️ Authentication](#authentication)
- [🚀 Deployment](#deployment)
- [🧪 Testing](#testing)
- [⚠️ Error Handling](#error-handling)
- [📈 Logging & Monitoring](#logging--monitoring)
- [📜 License](#license)

---

## Prerequisites 🛠️

Make sure you have the following tools installed:

- **Node.js** (v14.x or higher) 🌍
- **TypeScript** (v4.x or higher) 🔤
- **PostgreSQL** (v12.x or higher) 🗃️
- **Docker** (for containerization) 🐋
- **AWS** (for hosting the service) ☁️

---

## Installation 🚧

### 1. Clone the repository

```bash
git clone https://github.com/your-org/payment-service.git
cd payment-service
```

### 2. Install dependencies

```bash
npm install
```

### 3. Set up environment variables 🌍

Copy the `.env.example` to `.env` and fill out your configuration details like Paystack API key and database credentials.

```bash
cp .env.example .env
```

Here’s what you’ll need to set in your `.env`:

- `PAYSTACK_SECRET_KEY` – Paystack API secret key 🔑
- `DATABASE_URL` – PostgreSQL connection string 🛢️
- `JWT_SECRET` – Secret key for JWT token signing 🛡️
- `AWS_ACCESS_KEY_ID` – AWS access key for deployments 🏗️

---

## Endpoints 🔌

Here are the key API endpoints for the Payment Service:

### **1. `/payment/webhook`** 📲  
Webhook to receive payment status updates from Paystack.

**Method**: `POST`  
**Payload**: The Paystack webhook payload with payment status.

---

### **2. `/payment/initialize`** 💸  
Initialize a new payment request.

**Method**: `POST`  
**Request Body**:
```json
{
  "amount": 10000,
  "currency": "NGN",
  "email": "user@example.com",
  "reference": "unique-transaction-id"
}
```

**Response**:  
- `status`: URL to redirect the user for payment.

---

### **3. `/wallet/create`** 💰  
Create a wallet for a vendor.

**Method**: `POST`  
**Request Body**:
```json
{
  "vendor_id": "unique-vendor-id"
}
```

**Response**:  
- `status`: Success message for wallet creation.

---

### **4. `/wallet/balance`** 💳  
Retrieve wallet and escrow balances for the authenticated user.

**Method**: `GET`  
**Headers**:
- `Authorization`: Bearer token from the User Service

**Response**:
```json
{
  "balance": 5000,
  "escrow_balance": 1000
}
```

---

### **5. `/wallet/debit`** 💳  
Debit the wallet of the authenticated user.

**Method**: `POST`  
**Request Body**:
```json
{
  "amount": 1000
}
```

**Response**:  
- `status`: Success or failure message indicating debit status.

---

## Authentication 🛡️

All requests require JWT authentication. Tokens are issued by the **User Service** upon user login. Include the token in the `Authorization` header:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Deployment 🚀

This service is containerized using **Docker** and deployed on **AWS** via **Docker Compose**. For smooth deployment, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker-compose build
   ```

2. **Start the service:**

   ```bash
   docker-compose up payment-service -d
   ```

3. **CI/CD**: This service uses **GitHub Actions** for automated builds and deployments.

---

## Error Handling ⚠️

This service doesn’t have a formalized error handling strategy yet. Future improvements should include structured error codes and descriptive error messages for better debugging.

A standard error response could look like this:
```json
{
  "status": 400,
  "message": "Detailed error message"
}
```