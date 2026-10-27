# Valhala Games

A game management and transaction tracking web application built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **Jinja2**. The application provides a foundation for managing games, recording transactions, and controlling access to protected pages through user authentication and role-based permissions.

## Features

- **User authentication:** User registration and login with password hashing.
- **Session management:** Maintains authenticated user sessions.
- **Role-based access control:** Restricts protected pages and operations according to user roles.
- **Game management:** Supports adding games and managing their availability.
- **Transaction management:** Records transactions associated with games.
- **Payment methods:** Supports configurable payment methods, including bank transfer and Landmark App.
- **Server-rendered interface:** Uses Jinja2 templates to render pages.
- **Reusable layouts:** Shares navigation and page layouts through template inheritance.
- **Database integration:** Uses SQLAlchemy ORM with MySQL.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| FastAPI | Web framework |
| SQLAlchemy | Database ORM |
| MySQL | Relational database |
| PyMySQL | MySQL database driver |
| Jinja2 | Server-side HTML templates |
| Starlette Sessions | Cookie-based session management |
| Passlib with Argon2 | Password hashing |
| Uvicorn | ASGI server |




## Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.12 or later
- MySQL Server
- Git

### 2. Clone the Repository

```bash
git clone `https://github.com/SixtusNnanna/financialregister.git`
cd gamesVahala
```

Replace `https://github.com/SixtusNnanna/financialregister.git` with your actual Git repository URL.

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

If your project has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies used by your application, for example:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pymysql jinja2 python-multipart itsdangerous "passlib[argon2]"
```

Save the installed dependencies after confirming your environment is correct:

```bash
pip freeze > requirements.txt
```


### 5. Run the Application

From the project root, run the command that matches your application structure.

If your FastAPI instance is defined in `app/main.py` as `app`:

```bash
uvicorn app.main:app --reload
```

If your entry point is instead a root-level `main.py`, adjust the import path accordingly.

Open the application at:

- Application: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## Authentication and Authorization

The application uses session-based authentication to identify logged-in users.

After successful authentication, the user's ID is stored in the session. Protected endpoints retrieve the user from the database and can enforce access restrictions through role-based dependencies.

Example:

```python
Depends(require_roles(Role.ADMIN))
```

Public registration should assign a default role on the server rather than allowing users to grant themselves administrative privileges.



## Future Improvements

Potential improvements include:

- Automated tests for authentication, authorization, games, and transactions.
- Alembic database migrations.
- Transaction filtering and reporting.
- Pagination for transaction history.
- Improved validation and error handling.
- Docker-based development and deployment.
- Continuous integration and automated deployment.

No license has been specified yet. Add a license before distributing or accepting reuse of this project.
