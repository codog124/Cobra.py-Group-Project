from pydantic import BaseModel
from typing import Optional


# 🔹 Shared fields
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None


# 🔹 Create
class ProductCreate(ProductBase):
    pass


# 🔹 Update (all optional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None


# 🔹 Read (response)
class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True