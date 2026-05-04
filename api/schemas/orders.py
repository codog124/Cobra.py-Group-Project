from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderBase(BaseModel):
    tracking_number: Optional[str] = None
    user_id: Optional[int] = None

    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_address: Optional[str] = None

    status: Optional[str] = "Received"
    total_price: Optional[float] = None
    order_type: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
