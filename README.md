
# [AN ECOMMERCE MVP] - Backend

## Introduction
This is the backend API for a multi-vendor e-commerce platform. It provides a robust set of RESTful API endpoints for managing products, categories, orders, and user authentication.

## Features
-   User authentication with JWT (JSON Web Tokens).
-   Seller and Admin user roles.
-   CRUD operations for products and categories.
-   Order management system.
-   Custom Django management commands for database population.
-   Image handling via Cloudinary API.

## Technologies Used
-   **Backend Framework:** Django, Django REST Framework
-   **Programming Language:** Python
-   **Database:** PostgreSQL
-   **Database Hosting:** Neon Tech
-   **Containerization:** Docker
-   **Image Hosting:** Cloudinary
-   **Deployment:** Render

## Setup and Installation
To run this project locally, follow these steps:

1.  Clone the repository:
    ```sh
    git clone [https://github.com/Appyouz/ecommerce_backend.git](https://github.com/Appyouz/ecommerce_backend.git)
    cd ecommerce_backend
    ```

2.  Set up your environment variables. You will need:
    -   `SECRET_KEY`
    -   `DATABASE_URL`
    -   `CLOUDINARY_URL`
    -   `CLOUDINARY_CLOUD_NAME`
    -   `CLOUDINARY_API_KEY`
    -   `CLOUDINARY_API_SECRET`
    -   `DJANGO_ALLOWED_HOSTS`
    -   `DJANGO_CORS_ALLOWED_ORIGINS`
    -   `DJANGO_CSRF_TRUSTED_ORIGINS`

3.  Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```
    This will set up the PostgreSQL database and run the Django server.

4.  Run database migrations:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

5.  Create a superuser to access the admin panel:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## API Endpoints
All API endpoints are prefixed with `/api/`.

| Endpoint | Method | Description |
|---|---|---|
| `/products/` | `GET`, `POST` | List all products or create a new product. |
| `/products/{id}/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a single product. |
| `/categories/` | `GET`, `POST` | List all categories or create a new category. |
| `/orders/` | `GET`, `POST` | List all orders or create a new order. |
| `/token/` | `POST` | Get a JWT access and refresh token. |
| `/token/refresh/` | `POST` | Refresh a JWT access token. |

---


Frontend repo for this backen:[ecommerce_frontend](https://github.com/Appyouz/ecommerce_frontend)
