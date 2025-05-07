from typing import List, Optional

from sqlalchemy.orm import Session

from app.adapters.models.sql.product_model import ProductModel
from app.domain.entities.product import Product, ProductDb
from app.domain.interfaces.product_repository import ProductRepository


class SQLProductRepository(ProductRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> List[ProductDb]:
        products = self.db_session.query(ProductModel).all()
        return [self._map_to_entity(product) for product in products]

    def get_by_id(self, product_id: int) -> Optional[ProductDb]:
        product = self.db_session.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._map_to_entity(product) if product else None

    def create(self, product: Product) -> ProductDb:
        db_product = ProductModel(
            name=product.name,
            description=product.description,
            category=product.category,
            price=product.price,
            quantity=product.quantity
        )
        self.db_session.add(db_product)
        self.db_session.commit()
        self.db_session.refresh(db_product)
        return self._map_to_entity(db_product)

    def update(self, product_id: int, product: Product) -> Optional[ProductDb]:
        db_product = self.db_session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not db_product:
            return None
        
        db_product.name = product.name
        db_product.description = product.description
        db_product.category = product.category
        db_product.price = product.price
        db_product.quantity = product.quantity
        
        self.db_session.commit()
        self.db_session.refresh(db_product)
        return self._map_to_entity(db_product)

    def delete(self, product_id: int) -> bool:
        db_product = self.db_session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not db_product:
            return False
        
        self.db_session.delete(db_product)
        self.db_session.commit()
        return True
    
    def _map_to_entity(self, model: ProductModel) -> ProductDb:
        return ProductDb(
            id=model.id,
            name=model.name,
            description=model.description,
            category=model.category,
            price=model.price,
            quantity=model.quantity,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 