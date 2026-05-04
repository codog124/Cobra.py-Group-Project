from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Standard lengths for names and usernames
    name = Column(String(255))
    username = Column(String(50), unique=True, nullable=False)

    # Email and Phone updated with specific MySQL lengths
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)

    # Use Text for addresses to avoid the VARCHAR length requirement
    address = Column(Text, nullable=False)

    # Passwords should be long enough to hold hashes (bcrypt/argon2)
    password = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
