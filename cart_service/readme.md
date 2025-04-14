# Cart Service

## Overview

The **Cart Service** is a key component of the eCommerce platform, providing the necessary functionality for users to manage their shopping carts. This service handles operations like adding, updating, and removing items from the cart, checking stock availability, and maintaining user-specific cart data. It also integrates with other services for order creation and abandoned cart tracking. The service is built using Python and Django REST Framework, containerized with Docker, and orchestrated within a Docker Compose setup.

## Table of Contents

1. [General Information](#general-information)
2. [Core Functionality](#core-functionality)
3. [Inter-Service Communication](#inter-service-communication)
4. [Permissions & Roles](#permissions-roles)
5. [Data Storage](#data-storage)
6. [Async Operations](#async-operations)
7. [Payment Integration](#payment-integration)
8. [API Documentation](#api-documentation)
9. [Development & Deployment](#development-deployment)
10. [Other Considerations](#other-considerations)

## General Information

- **Language/Framework**: Python, Django REST Framework (DRF)
- **Containerization**: Dockerized, part of a larger microservice architecture using Docker Compose.
- **API**: Exposes a REST API for interaction with external services and users.
- **Database**: PostgreSQL for persistent data storage.
- **External Services**: Redis for abandoned cart tracking and background jobs.
- **Inter-Service Communication**: 
  - gRPC for communication with the Product Service to verify stock availability.
  - REST API calls to the Order Service for order conversion.

## Core Functionality

The **Cart Service** provides the following core functionalities:

- **Add/Remove Items**: 
  - Allows users to add and remove products from their shopping cart.
  - Provides basic validation and checks when adding/removing products.

- **Update Quantities**: 
  - Enables users to update the quantity of items in their cart.
  
- **View Cart**: 
  - Users can view the contents of their cart, including product details and total cost.

- **Stock Availability Check**: 
  - Verifies product availability by querying the Product Service via gRPC. Ensures the requested quantity is available before allowing users to add items to the cart.

- **Abandoned Cart Tracking**: 
  - Tracks abandoned carts using Redis, where carts with no activity for 24 hours are flagged.
  - After 24 hours, these abandoned carts are persisted to the PostgreSQL database.

- **Role-Based Access Control (RBAC)**:
  - Authenticated users (via JWT) can only modify their own cart.
  - Guests cannot modify any cart until authenticated.

## Inter-Service Communication

The **Cart Service** communicates with the following services:

- **Product Service** (via gRPC):
  - Queries product availability before adding items to the cart, ensuring the user cannot add more items than are available.

- **Order Service** (via REST):
  - Converts the cart to an order when the user proceeds to checkout.

- **User Service**:
  - Authentication information is embedded in the JWT token to identify the user making the request. No direct API calls are made to the User Service.

- **Payment Service**:
  - Not directly integrated with this service, but interacts with the Order Service for final payment processing.

## Permissions & Roles

- **RBAC (Role-Based Access Control)**:
  - Only authenticated users can interact with their cart.
  - Users can add, remove, and update items in their own cart, but not the cart of other users.
  - Guests are restricted from modifying any cart until they are logged in.

## Data Storage

- **PostgreSQL**: 
  - The main relational database for persisting cart data, including items, quantities, and user associations.
  
- **Redis**: 
  - Used for tracking abandoned carts. A cart is flagged as abandoned if it is inactive for 24 hours. Redis stores these carts temporarily before they are persisted to PostgreSQL.

## Async Operations

- **Abandoned Cart Tracking**:
  - Carts that remain inactive for more than 24 hours are considered abandoned. This is handled by a background task using Redis, and the data is periodically written to PostgreSQL.

- **Celery**: 
  - Utilized for handling background tasks like abandoned cart tracking and persistence.

## Payment Integration

- The **Cart Service** does not directly interact with the Payment Service. 
- The **Order Service** is responsible for initiating the payment process after the cart has been converted into an order.

## API Documentation

- **Swagger/OpenAPI**: Available at `/api/doc`.
- This provides comprehensive documentation for all endpoints, including descriptions, request/response formats, and examples.

## Development & Deployment

- **Docker Compose**: 
  - The service is part of a Docker Compose setup, allowing seamless orchestration with other services in the microservice architecture.
  
- **Environment Variables**:
  - Configuration details such as database connection strings and Redis credentials are managed through environment variables, stored in the `.env` file.

- **Async Task Management**: 
  - Celery is used to manage background tasks, particularly abandoned cart tracking.
  
- **Redis**: 
  - Redis is integral to the abandoned cart tracking mechanism and temporary data storage.

## Other Considerations

- **Audit Logs**: 
  - Changes made to the cart (e.g., items added/removed) are logged for auditing purposes.
  
- **Rate Limiting/Caching**: 
  - There is currently no rate limiting or caching implemented at the cart service level.

- **Multi-Tenancy**: 
  - The cart data is isolated per user. Users cannot access or modify the cart of other users.