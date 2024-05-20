# Market-Ecommerce

Market-Ecommerce is a web-based e-commerce platform built with Python using the Django framework and PostgreSQL as the database. This project provides a robust foundation for an online marketplace, including features such as user authentication, product management, and order processing.

## Features

- User registration and authentication
- Product listing and detailed views
- Shopping cart and order management
- Admin dashboard for managing products and orders

## Prerequisites

To run this application, you will need the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Django 3.2+](https://docs.djangoproject.com/en/stable/releases/3.2/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Azizbekdevn1/market-ecommerce.git
    ```
2. Navigate to the project directory:
    ```bash
    cd market-ecommerce
    ```
3. Set up a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory and add your database configuration and secret key:
    ```env
    SECRET_KEY='your_secret_key'
    DB_NAME='your_db_name'
    DB_USER='your_db_user'
    DB_PASSWORD='your_db_password'
    DB_HOST='localhost'
    DB_PORT='5432'
    ```
5. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser for accessing the Django admin interface:
    ```bash
    python manage.py createsuperuser
    ```
7. Collect static files:
    ```bash
    python manage.py collectstatic
    ```

## Running the Application

To run the development server, use the following command:
```bash
python manage.py runserver
