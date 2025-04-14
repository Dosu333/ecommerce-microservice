# 🧑‍💼 User Service — eCommerce Microservices Platform

The **User Service** is responsible for authentication, authorization, and user identity management within the eCommerce platform. It provides RESTful APIs for registration, login, role-based access, and JWT token lifecycle management for customers, vendors, and admins.

---

## 🔧 Tech Stack

- **Language & Framework**: Python 3.10+, Django 5.x, Django REST Framework (DRF)
- **Authentication**: JWT (access + refresh tokens)
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Deployment**: AWS (via Docker Compose)
- **CI/CD**: GitHub Actions
- **API Docs**: Swagger/OpenAPI (accessible at `/api/doc`)
- **Testing**: Django `APITestCase` (DRF)

---

## 📦 Features

- ✅ User registration and login
- 🔐 JWT-based authentication (access + refresh token flow)
- ♻️ Refresh token endpoint
- 🧑‍💻 Role-based access control (Customer, Vendor, Admin)
- 🔐 Password reset workflow
- 📓 Audit logging (basic)
- 🔥 Local dev hot-reloading
- 📘 Swagger docs at `/api/doc`

---

## 🔐 Authentication Flow

- **JWT Access Token**: Short-lived; used to access protected endpoints
- **JWT Refresh Token**: Long-lived; used to obtain new access tokens
- **Token Rotation**: When the refresh token expires, the user must re-login
- **Roles Supported**:
  - `CUSTOMER`
  - `VENDOR`
  - `ADMIN`

---

## 🛠️ Local Development

### Prerequisites

- Docker + Docker Compose
- Python 3.10+
- PostgreSQL (Docker handles this)

### Spin Up Services

```bash
docker-compose up --build
```

The service will be available at `http://localhost:8000`.

### API Documentation

```http
GET http://localhost:8000/api/doc
```

---

## 🔁 API Endpoints

| Method | Endpoint              | Description                         | Auth Required |
|--------|-----------------------|-------------------------------------|---------------|
| POST   | `/api/auth/users` | Register a new user                 | ❌            |
| POST   | `/api/auth/login`    | Login and receive JWT tokens        | ❌            |
| POST   | `/api/auth/token/refresh`  | Refresh JWT token                   | ✅ (refresh)  |
| POST   | `/api/auth/users/reset-password` | Start password reset workflow | ❌            |
| GET    | `/api/auth/users/create-password`       | Create password from reset token     | ❌            |

> For full API usage, refer to the Swagger docs at `https://ecommerceuser.oladosularinde.com/api/doc`.

---

## 🧪 Running Tests

```bash
docker-compose exec user-service python manage.py test
```

Tests use `APITestCase` from Django REST Framework.

---

## 🚀 Deployment

The service is deployed with Docker Compose to AWS.

> Environment variables and secrets are managed via a `.env` file (see below).

---

## 🔑 Environment Variables

There is a sample `.env` file structure (refer to `.env.sample` for the complete list):

---

## 🧩 Integrations

- Communicates with other services (Cart, Order, Payment, Product) via REST APIs
- Emits/Consumes no events currently (no pub/sub, message queues)

---

## 🛡️ Security Notes

- 🔐 RBAC is enforced at the view level using custom DRF permissions
- ❌ No rate limiting is enabled yet — recommended to add DRF throttling or middleware
- ⚠️ Tokens are signed but not blacklisted (no revocation list)
- 🔍 Audit logging is basic — extend with structured logging for compliance

---

## 📌 Future Improvements

- Add support for Google/Facebook OAuth
- Introduce rate limiting and request throttling
- Blacklist JWT refresh tokens on logout
- Add full audit logging and event-driven user lifecycle (e.g., registration events)