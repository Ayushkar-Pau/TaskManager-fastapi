# TaskManager-fastapi
A production-grade, modular Task Management API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This project demonstrates a clean architecture, secure authentication, and owner-based data isolation.

---

## Architecture
This project follows a **Modular Design** to ensure scalability and maintainability:
- **Routers**: Separated by domain (Auth, Tasks, Users).
- **Models**: Database tables defined via SQLAlchemy.
- **Schemas**: Data validation and serialization using Pydantic.
- **Dependencies**: Centralized security logic and database session management.

---

## Key Features
* **Secure Authentication**: User registration and login using hashed passwords (Bcrypt) and JWT tokens.
* **Task Management**: Full CRUD operations for tasks.
* **Data Isolation**: Users can only access and manage their own tasks.
* **Admin Access**: Dedicated administrative routes for user management (restricted by email-based role check).
* **Automatic Docs**: Interactive API documentation via Swagger UI.

---

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Security**: JWT, Passlib (Bcrypt)
- **Validation**: Pydantic v2
- **Server**: Uvicorn

---

## Project structure
```text
TaskManager-fastapi/
├── app/
│   ├── routers/       # API endpoints (auth, tasks, users)
│   ├── db_models.py      # SQLAlchemy database models
│   ├── models.py     # Pydantic validation models
│   ├── database.py    # Database connection & session
│   ├── utils.py       # Hashing and JWT logic
│   ├── dependencies.py # Shared injection (get_current_user)
│   └── main.py        # Application entry point
├── .env
├── .gitignore         # Git ignore rules
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation