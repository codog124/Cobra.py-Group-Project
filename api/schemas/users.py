from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    phone: str
    address: str

class UserCreate(UserBase):
    email: Optional[str]
    password: Optional[str]

class UserResponse(UserBase):
    id: int
    is_guest: bool

    class Config:
        from_attributes = True
