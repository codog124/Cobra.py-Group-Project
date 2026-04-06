from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    method: str
    status: str
    amount: float

class PaymentCreate(PaymentBase):
    order_id: int

class PaymentUpdate(BaseModel):
    method: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None

class PaymentRead(PaymentBase):
    id: int
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True
