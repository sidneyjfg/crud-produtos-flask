from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin
from . import Base

class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
