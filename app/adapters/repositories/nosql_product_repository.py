from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection

from app.adapters.models.nosql.connection import product_collection
from app.domain.entities.product import Product, ProductDb
from app.domain.interfaces.product_repository import ProductRepository


class NoSQLProductRepository(ProductRepository):
    def __init__(self, collection: Collection = product_collection):
        self.collection = collection

    def get_all(self) -> List[ProductDb]:
        products = list(self.collection.find())
        return [self._map_to_entity(product) for product in products]

    def get_by_id(self, product_id: int) -> Optional[ProductDb]:
        product = self.collection.find_one({"_id": product_id})
        return self._map_to_entity(product) if product else None

    def create(self, product: Product) -> ProductDb:
        # Find the highest id to simulate auto-increment
        last_product = self.collection.find_one(sort=[("_id", -1)])
        next_id = 1 if not last_product else last_product["_id"] + 1
        
        now = datetime.utcnow()
        product_dict = {
            "_id": next_id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "quantity": product.quantity,
            "created_at": now,
            "updated_at": now
        }
        
        self.collection.insert_one(product_dict)
        return self._map_to_entity(product_dict)

    def update(self, product_id: int, product: Product) -> Optional[ProductDb]:
        now = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": product_id},
            {"$set": {
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "quantity": product.quantity,
                "updated_at": now
            }}
        )
        
        if result.modified_count == 0:
            return None
            
        return self.get_by_id(product_id)

    def delete(self, product_id: int) -> bool:
        result = self.collection.delete_one({"_id": product_id})
        return result.deleted_count > 0
    
    def _map_to_entity(self, data: dict) -> ProductDb:
        return ProductDb(
            id=data["_id"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        ) 