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