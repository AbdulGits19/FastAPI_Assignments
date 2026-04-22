# Healthcare Management System API

## Project Overview

This project is a modularized backend application built using FastAPI and Python 3.14. It provides a comprehensive system for managing a hospital's operations, including tracking doctors, patients, and scheduled appointments. The application is built with a focus on security, persistent data storage, and efficient data retrieval through pagination and filtering.

## Core Features

  * **Doctor Management**: Full CRUD operations for medical staff including specialization and availability tracking.
  * **Patient Records**: Secure management of patient demographics and contact information.
  * **Appointment System**: A relational module that links doctors and patients to specific time slots with status tracking.
  * **Authentication and Security**: Implements JWT-based (JSON Web Token) authentication using the PBKDF2 algorithm for secure password hashing.
  * **Search and Filtering**: Advanced endpoints to filter medical staff by specialization and search for patients by name or phone number.
  * **Pagination**: Optimized data fetching for large lists of records using limit and offset parameters.

## Technical Architecture

  * **Framework**: FastAPI.
  * **Database**: SQLite with SQLAlchemy ORM for permanent data persistence.
  * **Security**: OAuth2 with Bearer tokens and JWT encryption.
  * **Project Structure**: Modular design with separated concerns for models, schemas, and authentication logic.

## Installation and Setup

1.  Clone the repository and navigate to the project directory.
2.  Install the required dependencies:
    ```bash
    pip install fastapi uvicorn sqlalchemy passlib python-jose[cryptography] python-dotenv
    ```
3.  Ensure your .env file contains the necessary configuration for the SECRET\_KEY and ALGORITHM.
4.  Launch the application:
    ```bash
    python -m uvicorn app.main:app --reload
    ```

## API Documentation and Testing

The system includes interactive documentation for testing all endpoints:

1.  Access the documentation at [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs).
2.  Register a new administrative account via the /register endpoint.
3.  Use the /token endpoint or the Authorize button to generate an access token.
4.  Once authorized, protected routes (Create, Update, Delete) will be accessible.
