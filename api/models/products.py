from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from ..dependencies.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    # New field for inventory check
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True) # For "deleting" without losing history
    category_id = Column(Integer, ForeignKey("categories.id"))