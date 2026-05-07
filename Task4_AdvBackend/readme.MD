Task4_Advanced/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry Point: FastAPI init & Error Handlers[cite: 6]
│   │   ├── database.py          # SQLAlchemy Engine & Session[cite: 5]
│   │   ├── models.py            # DB Models: Roles & Statuses
│   │   ├── schemas.py           # Pydantic: Auth, Pagination & Standardization[cite: 8]
│   │   ├── auth.py              # JWT Logic & get_current_active_user[cite: 4]
│   │   ├── routers/             # THIN ROUTERS: No business logic here
│   │   │   ├── auth.py          # Login, Register, Forgot Password
│   │   │   ├── doctors.py       # Search, Filter, & CRUD
│   │   │   ├── patients.py      # Patient Management
│   │   │   └── appointments.py  # Booking & Status Updates[cite: 9]
│   │   ├── services/            # THE BRAIN: All Business Logic[cite: 1]
│   │   │   ├── auth_service.py      # Registration, Hashing, Forgot Password logic
│   │   │   ├── doctor_service.py    # Pagination, Sorting, & Filtering logic
│   │   │   └── appointment_service.py # Double-booking & Slot validation logic
│   │   ├── utils/               # HELPERS
│   │   │   ├── deps.py          # RBAC (is_admin, is_doctor) dependencies
│   │   │   ├── security.py      # Password hashing (Bcrypt) helpers[cite: 4]
│   │   │   └── file_handler.py  # File size/type validation logic
│   │   ├── tasks.py             # BackgroundTasks (Async Notifications)
│   │   └── websocket.py         # Real-time alerts[cite: 8]
│   ├── tests/                   # PYTEST: Automated Unit Tests
│   │   ├── conftest.py          # Test DB setup
│   │   └── test_main.py         # Testing RBAC & Logic
│   ├── .env                     # Secret Keys & DB Config[cite: 2]
│   └── requirements.txt         # Dependencies




# Hospital Management System - Advanced Backend

This project is the probable final task for the FastAPI Advanced Backend module. It implements a secure medical management system with role-based access control, automated conflict handling for appointments, and validated file management.

## Project Structure
The code is organized using a service-layer pattern to keep the logic separate from the API routes. 
- /app/routers: Contains all the API endpoints.
- /app/services: Handles the business logic (like checking for double-bookings).
- /app/models: Defines the SQLite database structure.
- /app/schemas: Pydantic models for data validation and serialization.
- /app/utils: Helper functions for authentication and file validation.

## Key Features
- **Authentication**: Uses JWT tokens with Bcrypt password hashing.
- **RBAC**: Three distinct roles (Admin, Doctor, Patient) with specific permissions.
- **Appointments**: Logic to prevent double-booking the same doctor at the same time.
- **File Handling**: Upload system for patient reports that validates file extension and size (Max 5MB).
- **Pagination**: Implemented on Doctor and Patient list views to handle large datasets.
- **Background Tasks**: Simulated email notifications triggered when appointment statuses change.

## Installation and Setup
1. Create a virtual environment: `python -m venv .venv`
2. Activate the environment: `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python -m uvicorn Backend.app.main:app --reload`

## Testing
To run the automated test suite, use the following command from the root directory:
python -m pytest

The tests cover basic endpoint connectivity and verify that unauthorized users are blocked from restricted routes.
