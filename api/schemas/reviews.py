from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    user_id: int
    menu_item_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    menu_item_id: int

    class Config:
        from_attributes = True
