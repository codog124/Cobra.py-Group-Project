from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    guest_name = Column(String)
    guest_phone = Column(String)
    guest_address = Column(String)

    status = Column(String, default="Received")
    total_price = Column(Float)
    order_type = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
