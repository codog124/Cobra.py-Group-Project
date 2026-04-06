from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
  name: str
  description: Optional[str] = None
  ingredients: Optional[str] = None
  price: float
  calories: Optional[int] = None
  category_id: Optional[int] = None

class MenuItemCreate(MenuItemBase):
  pass

class MenuItemUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  ingredients: Optional[str] = None
  price: Optional[float] = None
  calories: Optional[int] = None
  category_id: Optional[int] = None

class MenuItem(MenuItemBase):
  id: int

  class Config:
    from_attributes = True
