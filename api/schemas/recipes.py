from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .sandwiches import Sandwich


class RecipeBase(BaseModel):
    sandwich_id: int
    resource_id: int
    amount: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int

    class ConfigDict:
        from_attributes = True
