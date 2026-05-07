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