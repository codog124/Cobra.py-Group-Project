from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    menu_item = relationship("MenuItem", back_populates="order_items")
    order = relationship(
        "Order",
        back_populates="order_items"
    )