# 🛒 Product Service

The **Product Service** is a core component of the eCommerce microservices architecture, responsible for managing product catalogs, categories, stock tracking, and product discovery (search, filter, and sort). It is built with Django REST Framework, containerized using Docker, and communicates with other services via gRPC and REST.

---

## 🚀 Overview

- **Language:** Python  
- **Framework:** Django REST Framework  
- **Architecture:** Microservices (Monorepo)  
- **API Type:** RESTful + gRPC (for internal service-to-service communication)  
- **Database:** MongoDB  
- **Containerized:** ✅ Docker  
- **Orchestrator:** Docker Compose  
- **Search:** Full-text search via query param `?search=`  
- **Docs:** Swagger/OpenAPI at `/api/doc`

---

## 🧑‍💻 Core Features

| Feature | Description |
|--------|-------------|
| **Product CRUD** | Vendors can create, update, and delete products. |
| **Category Management** | Vendors can manage their own categories. |
| **Public Product Listings** | Customers can list and view products and categories. |
| **Role-Based Access** | Endpoints enforce permissions for customers, vendors, and admins. |
| **Stock Tracking** | Tracks product inventory. |
| **Media Uploads** | Uses **Cloudinary** for image hosting. Uploads are async with WebSocket progress updates. |
| **Search, Filter & Sort** | Products can be filtered, sorted, and searched by name/description. |
| **Real-Time Notifications** | WebSocket support for frontend sync post image upload. |

---

## 🔁 Inter-Service Communication

This service uses **gRPC** to interact with other internal services for seamless coordination:

- **Cart Service:**  
  - Validate if a product exists when added to cart.
  - Sync stock info during cart changes.

- **Order Service:**  
  - Reduce stock count on successful order placement.
  - Validate product availability during checkout.

All external/public interactions are via **REST API**, while internal service-to-service calls are via **gRPC** to improve efficiency and type safety.

---

## 🔐 Authentication & Authorization

- **Authentication:** JWT (provided by User Service)
- **Authorization:** Role-Based (RBAC)
  - **Vendors** → Full access to their products and categories
  - **Customers** → Can view products and categories
  - **Admins** → Platform-level oversight if needed

---

## 🗃️ Data Storage

- **Database:** MongoDB
- **Media Storage:** Cloudinary
- **Relationships:** Products are associated with categories and vendors
- **Tenancy:** Products are isolated per vendor (multi-tenancy style)

---

## 🧪 Testing

- **Framework:** [pytest](https://docs.pytest.org/)
- **Coverage:** Unit and integration tests for product lifecycle, permissions, and gRPC interactions

---

## 📘 API Documentation

- **Docs URL:** `http://localhost:<port>/api/doc`
- **Format:** Swagger/OpenAPI
- **Auth Required:** Yes, for all write operations

---

## 🧰 Dev & Deployment

- **Hot Reloading:** Supported in local dev
- **Containerized:** ✅
- **Orchestration:** Docker Compose with other services
- **Cloud:** AWS
- **Env Config:** See `.env.sample` for variables like:
  - `CLOUDINARY_API_KEY`
  - `MONGO_URI`
  - `GRPC_CART_SERVICE_HOST`
  - `GRPC_ORDER_SERVICE_HOST`

---

## 🧠 Additional Notes

| Feature | Status |
|--------|--------|
| **Multi-Tenancy** | ✅ Vendors only manage their own products |
| **Audit Logs** | ✅ Available |
| **Rate Limiting** | ❌ Not implemented |
| **Caching** | ❌ No Redis-based caching |
| **gRPC** | ✅ Communicates with Cart and Order Services |
| **WebSockets** | ✅ Used for media upload feedback |

---

## 🛠 Future Work

- Add Redis caching for high-traffic product listings
- Implement rate limiting on listing endpoints
- Auto-sync product stock from order/cancellation workflows
- Add dedicated search API with weights
