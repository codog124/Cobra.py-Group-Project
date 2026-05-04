from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderDetailBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_address: Optional[str] = None
    order_type: str

class OrderCreate(OrderBase):
    promo_code: Optional[str] = None
    items: List[OrderDetailBase]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    guest_name: Optional[str] = None
    guest_address: Optional[str] = None

class Order(OrderBase):
    id: int
    tracking_number: str
    status: str
    total_price: float
    order_date: datetime

    class Config:
        from_attributes = True