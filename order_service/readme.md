# 🧾 Order Service

The **Order Service** is a critical component of the eCommerce microservices ecosystem. It handles all operations related to order placement, tracking, management, and integration with other services such as Cart, Product, Payment, and User.

---

## 🧑‍💻 1. General Overview

- **Language & Framework:** Python — [Django REST Framework](https://www.django-rest-framework.org/)
- **API Protocols:**  
  - REST (external + internal APIs)  
  - gRPC (inter-service communication)  
  - Redis Pub/Sub (for messaging with the Payment Service)
- **Database:** PostgreSQL (via Django ORM)
- **Containerization:** Dockerized and orchestrated using **Docker Compose**
- **Repository Layout:** Part of a **monorepo** with other services

---

## 📦 2. Core Features

- **Order Placement:** Customers can place orders using the contents of their cart
- **Order History:** Users can view past orders with pagination and filters
- **Cancel Order:** Orders can be canceled before processing begins
- **Delivery Tracking:** Orders include status updates (e.g., pending, shipped, delivered)
- **Vendor Dashboard:** Vendors can view/manage orders containing their products
- **Payment Integration:** Communicates with Payment Service to verify and track payments

---

## 🔁 3. Inter-Service Communication

| Service         | Purpose                          | Method        |
|-----------------|----------------------------------|---------------|
| **User Service**    | Fetch customer/vendor/admin info     | REST API      |
| **Product Service** | Stock verification, price sync       | gRPC          |
| **Cart Service**    | Load cart items during checkout      | REST API      |
| **Payment Service** | Payment confirmation & status        | Redis Messaging |

---

## 🔐 4. Authentication & Authorization

- **Authentication:** JWT-based, validated via middleware
- **Role-Based Access Control (RBAC):**
  - **Customer:** Can place, view, and cancel personal orders
  - **Vendor:** Can view/manage orders for their products
  - **Admin:** Full visibility and control across all orders

---

## 🗃️ 5. Database & Persistence

- **DB Engine:** PostgreSQL  
- **ORM:** Django ORM  
- **Schema Includes:**
  - `Order`
  - `OrderItem`
- Relationships are maintained with foreign keys (e.g., user, product, vendor)

---

## 📘 6. API Documentation

- **Docs URL:** `/api/doc`
- **Tool:** Swagger / drf-yasg
- **Authentication:** JWT-based via Swagger UI support
- **Highlights:**
  - Searchable and interactive endpoints
  - Filter, sort, and paginate orders
  - Role-specific access info embedded in documentation

---

## 🧰 7. Dev & Deployment

- **Environment Variables:**
  - See `.env.sample` for full list
  - Includes DB credentials, Redis URL, and messaging configs
- **Background Jobs:**
  - Uses **Celery** with Redis as the broker
  - E.g., clearing cart asynchronously post-order
- **Deployment Stack:**
  - Docker Compose
  - Deployed on **AWS**

---

## 🧠 8. Other Notes

- **Audit Logging:** Tracks key order lifecycle events (created, updated, canceled, status change)
- **Multi-Tenancy Support:**
  - Vendor views scoped to only their products
  - Admin has global access
- **No Caching or Rate Limiting:** Can be added via Django middleware or reverse proxy (e.g., NGINX)
- **Scalability:** Designed for easy horizontal scaling using queues and gRPC

---

## 🚀 9. Future Work
- Discounts & Coupons: Introduce a discount and coupon management system for customers to apply discounts to their orders.
- Order Analytics: Provide advanced analytics on orders, such as popular products, sales trends, and customer buying patterns.
- Rate Limiting & Caching: Implement rate limiting and caching to improve performance, especially for high-traffic endpoints (e.g., order placement).
