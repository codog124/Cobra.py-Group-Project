from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PromotionBase(BaseModel):
    code: str
    discount_percent: float
    expiration_date: datetime
    active: bool = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[float] = None
    expiration_date: Optional[datetime] = None
    active: Optional[bool] = None

class PromotionRead(PromotionBase):
    id: int

    class Config:
        from_attributes = True
