from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User  # noqa
from .product import Product  # noqa
