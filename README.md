![Logo](./img%20&%20videos/Group%205.png)

> [!NOTE]
> This project was created to reinforce knowledge on WebSocket and JWT (JSON Web Token)

## Technologies used:

* **FastAPI** — the main backend framework responsible for routing, dependency injection, authentication handling, and WebSocket support.

* **PostgreSQL + SQLAlchemy** — used for database storage and ORM interaction, including user authentication and role management.

* **JWT (JSON Web Token)** — provides secure authentication for both HTTP endpoints and WebSocket connections. Tokens store user identity and role information.

* **WebSocket** — enables real-time chat functionality.
  Includes:

  * connection management,
  * message broadcasting,
  * personal messages,
  * moderation commands (ban, mute, kick, warn),
  * forbidden-word filtering.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Marchello-Projects/WebSockChat_by_Marchello
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Set up environment variables

Create a `.env` file in the root directory with the following content:

```env
DATABASE_NAME=Database_Name
DB_USER=Database_username
DB_PASSWORD=Database_password
SECRET_KEY=Key_for_JWT
```

> [!NOTE]
> The key can be generated on the website: https://jwtsecrets.com/

### 5. Creating users:

```python
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import Session

from app.config.configdb import engine, Base, session_local


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default=UserRole.USER.value)



Base.metadata.create_all(bind=engine)


# ===== Default user creation =====
# def create_default_users():
#    db: Session = session_local()
#
#    # Check if default users already exist
#    admin_exists = db.query(User).filter(User.username == "Marchello").first()
#    user_exists = db.query(User).filter(User.username == "Linus").first()
#
#    # Create admin user
#    if not admin_exists:
#        admin = User(
#            username="Marchello",
#            password="adminpass",   # Change if needed
#            role=UserRole.ADMIN.value
#        )
#        db.add(admin)
#
#    # Create regular user
#    if not user_exists:
#        regular_user = User(
#            username="Linus",
#            password="userpass",    # Change if needed
#            role=UserRole.USER.value
#        )
#        db.add(regular_user)
#
#    db.commit()
#    db.close()
#
# create_default_users()
```

### 6. Obtaining JWT Tokens:
Run the project:

```bash
python3 -m app.main
```

Go to the Swagger documentation:

`http://127.0.0.1:8000/docs`

Then enter your username and password in the `/auth/login` endpoint:

![login](./img%20&%20videos/Запись%20экрана%20от%202025-12-10%2021-35-24.gif)

After that, copy the JWT token from the response

### 7. WebSocket Connection:

Run this command using two terminals and the two tokens you obtained:

```bash
websocat "ws://127.0.0.1:8000/ws/chat?token=YOUR_JWT_TOKEN"
```

> [!WARNING]
> Websocat must be installed. If it is not present on your system, you can download it from the following repository: https://github.com/vi/websocat?tab=readme-ov-file
