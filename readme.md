
# eCommerce Platform Overview 🚀

Welcome to the **eCommerce Platform** repository! This project consists of a set of microservices designed to power a robust, scalable, and flexible online store. Each service handles a specific part of the system, and together they provide the foundation for a seamless shopping experience.

---

## Table of Contents 📚

- [🌟 Overview](#overview)
- [🛠️ Microservices Architecture](#microservices-architecture)
- [⚙️ Technology Stack](#technology-stack)
- [🔒 Authentication & Authorization](#authentication--authorization)
- [📦 Installation & Setup](#installation--setup)
- [🚀 Deployment](#deployment)

---

## Overview 🌟

The **eCommerce Platform** is a set of interconnected microservices designed to manage users, products, orders, payments, and more. The services communicate through APIs, and each one is independently deployable, ensuring flexibility and scalability.

Each service focuses on a specific domain, and the platform as a whole enables smooth, efficient operations for an online store. Below is an overview of the key services:

### Key Services 🛠️

1. **User Service** 👤  
   Manages user registration, authentication, profiles, and account details. It’s responsible for issuing **JWT tokens** used across other services for authentication.

2. **Product Service** 📦  
   Handles everything related to products, including adding new products, updating inventory, managing categories, and exposing product listings through a public API.

3. **Cart Service** 🛒  
   Manages the user's cart. It allows users to add, remove, and modify products in their cart, maintaining a temporary session until checkout.

4. **Order Service** 📦  
   Processes user orders, maintains order history, and handles statuses (pending, shipped, delivered). It interacts with the **Payment Service** to finalize the transaction.

5. **Payment Service** 💳  
   Handles the processing of payments, integrates with external payment gateway (**Paystack**), and manages wallet operations (e.g., debiting accounts, wallet balance queries).

---

## Microservices Architecture 🏗️

The system is designed using a **microservices architecture**, which ensures modularity and ease of maintenance. Here’s how the services interact:

- **User Service** issues **JWT tokens**, which are used by other services for secure authentication.
- **Cart Service** and **Order Service** interact with the **Product Service** to retrieve product details for checkout.
- **Payment Service** processes payments for orders through external gateway, **Paystack**.
- Each service has its own database and handles its own state.

---

## Technology Stack ⚙️

Each service is built with the following technologies:

- **Node.js** with **TypeScript** for the backend ⚡
- **Django** with for the backend ⚡
- **PostgreSQL** for relational data storage 🗃️
- **Docker** for containerization 🐋
- **AWS** for cloud hosting ☁️
- **GitHub Actions** for CI/CD 🤖
- **Paystack** for payment gateway integration 💸

---

## Authentication & Authorization 🔒

All services use **JWT tokens** for authentication and authorization. The tokens are issued by the **User Service** during the login process and are required for accessing protected endpoints across all services.

### Authentication Flow:

1. A user logs in through the **User Service** and receives a JWT token.
2. The user includes this token in the `Authorization` header for requests to services like **Cart**, **Order**, and **Payment**.
3. Each service verifies the token before processing the request.

---

## Installation & Setup 🛠️

To get started with the platform locally, follow the steps below:

### 1. Clone the repository

```bash
git clone https://github.com/Dosu333/ecommerce-microservice.git
cd ecommerce-platform
```

### 2. Set up Docker Compose

Make sure you have **Docker** and **Docker Compose** installed. Then, start all the services using:

```bash
docker-compose up --build
```

This will build and start all services in their respective containers. By default, the services will be available on different ports, and **PostgreSQL** will be set up for the **User Service**.

### 3. Set up Environment Variables 🌍

Each service requires environment-specific variables. You can configure them in the `.env` files for each service, or globally in the root `.env` file.

Key variables include:

- **JWT_SECRET** for token signing
- **PAYSTACK_SECRET_KEY** for the Payment Service
- **DATABASE_URL** for the database connection

---

## Deployment 🚀

The platform is designed to be deployed on **AWS** using **Docker Compose**. The services are containerized, and you can deploy them with **GitHub Actions** for continuous deployment.

Steps to deploy:

1. **Build the Docker images**:
   ```bash
   docker-compose build
   ```

2. **Deploy the services** to your AWS environment:
   Follow the GitHub Actions workflow configured for automatic deployment.

3. **Configure environment variables** in your AWS environment to match those specified in the `.env.example` files.