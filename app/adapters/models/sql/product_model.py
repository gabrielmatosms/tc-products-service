from sqlalchemy import Column, Float, Integer, String

from app.adapters.models.sql.base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0) 