# WebShop

**WebShop** is a Python Django-based e-commerce platform that offers features like user authentication, product browsing, filtering, cart management, and secure order checkout. It integrates an AI-powered assistant using the OpenAI API for smart product retrieval, ensuring relevant and accurate product recommendations based on user queries.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [Authentication API](#authentication-api)
  - [Product API](#product-api)
  - [Cart API](#cart-api)
  - [Order API](#order-api)
  - [AI Assistant API](#ai-assistant-api)
- [Next Steps](#next-steps)

## Features

- **User Authentication**: Register, login, logout, and manage user profiles.
- **Product Management**: Browse, search, filter, and create products.
- **Cart System**: Add, remove, update items in the cart and view cart details.
- **Order Management**: Place and track orders, with options to update order status.
- **AI-Powered Product Retrieval**: Intelligent product recommendations using the OpenAI API based on user queries.
- **Responsive Design (Upcoming)**: To be integrated with a frontend framework like React, Angular, or Vue.

## Tech Stack

- **Backend**: Django (Python)
- **Database**: MongoDB
- **AI Integration**: OpenAI API for intelligent product recommendations
- **Others**:
  - Django REST Framework (for API endpoints)
  - JWT (for secure authentication)
  - Pipenv (for environment and dependency management)

## Setup and Installation

### Prerequisites

- Python 3.x
- MongoDB instance (local or cloud)
- OpenAI API key (for AI assistant functionality)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sumitkevlani/webshop.git
   cd webshop
2. **Install Pipenv(if not already installed)**:
    ```bash
    pip install pipenv
3. **Install dependencies**:
    ```bash
    pipenv install
4. **Set up environment variables: Create a .env file in the root directory with the following**:
    ```bash
    SECRET_KEY=<your_django_secret_key>
    DEBUG=True
    MONGODB_HOST=<your_mongodb_host>
    MONGODB_NAME=<your_mongodb_database_name>
    MONGODB_USERNAME=<your_mongodb_username>
    MONGODB_PASSWORD=<your_mongodb_password>
    OPENAI_API_KEY=<your_openai_api_key> 
5. **Apply migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
6. **Run the development server**:
    ```bash
    python manage.py runserver
7. **Access the app**:
    Open your browser and navigate to http://127.0.0.1:8000/.

## Usage

### Authentication API
- `POST /api/auth/login/` – Login a user.
- `POST /api/auth/register/` – Register a new user.
- `POST /api/auth/logout/` – Logout the current user.
- `POST /api/auth/get-user/` – Retrieve the authenticated user's details.

### Product API
- `GET /api/product/get-products/` – Retrieve all products.
- `POST /api/product/create-product/` – Create a new product (admin only).

### Cart API
- `GET /api/cart/get-cart/` – Retrieve the current user's cart.
- `POST /api/cart/add-to-cart/` – Add an item to the cart.
- `DELETE /api/cart/remove-from-cart/` – Remove an item from the cart.
- `PUT /api/cart/update-cart/` – Update the quantity of an item in the cart.

### Order API
- `POST /api/orders/create-order/` – Create a new order.
- `GET /api/orders/get-my-orders/` – Retrieve the authenticated user's orders.
- `PUT /api/orders/update-order-status/<order_id>/` – Update the status of an order (admin only).

### AI Assistant API
- `GET /api/ai-assistant/query/` – Retrieve product recommendations based on user queries.

## Next Steps

- **Frontend Integration**: We plan to integrate a modern frontend framework such as React, Angular, or Vue to improve user experience and offer a dynamic interface.
  
- **Docker and Nginx**: Implement Docker for containerization and Nginx for serving the application in production environments.

- **CI/CD Pipeline**: Set up continuous integration and deployment using tools like GitHub Actions, Travis CI, or Jenkins to streamline the development and deployment process.
