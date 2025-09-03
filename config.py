from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = True
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
