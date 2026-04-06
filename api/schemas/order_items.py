from pydantic import BaseModel
from typing import Optional

class OrderItemBase(BaseModel):
  order_id: int
  menu_item_id: int
  quantity: int
  price: float

class OrderItemCreate(OrderItemBase):
  pass

class OrderItemUpdate(BaseModel):
  order_id: Optional[int] = None
  menu_item_id: Optional[int] = None
  quantity: Optional[int] = None
  price: Optional[float] = None

class OrderItem(OrderItemBase):
  id: int

  class Config:
    from_attributes = True
