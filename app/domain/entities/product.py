from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProductCategory(str, Enum):
    MAIN_ITEM = "Main Item"
    SIDE = "Side"
    DRINK = "Drink"
    DESSERT = "Dessert"


class Product(BaseModel):
    name: str
    description: str
    category: ProductCategory
    price: float
    quantity: int


class ProductDb(Product):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 