from typing import List, Optional

from app.domain.entities.product import Product, ProductDb
from app.domain.interfaces.product_repository import ProductRepository


class ProductUseCases:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self) -> List[ProductDb]:
        return self.repository.get_all()

    def get_product_by_id(self, product_id: int) -> Optional[ProductDb]:
        return self.repository.get_by_id(product_id)

    def create_product(self, product: Product) -> ProductDb:
        return self.repository.create(product)

    def update_product(self, product_id: int, product: Product) -> Optional[ProductDb]:
        # Check if product exists
        existing = self.repository.get_by_id(product_id)
        if not existing:
            return None
        
        return self.repository.update(product_id, product)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
        
    def update_product_quantity(self, product_id: int, quantity_change: int) -> Optional[ProductDb]:
        """Update product quantity by adding quantity_change (negative for decreasing)"""
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        
        # Create a copy of the product with updated quantity
        updated_product = Product(
            name=product.name,
            description=product.description,
            category=product.category,
            price=product.price,
            quantity=max(0, product.quantity + quantity_change)  # Ensure quantity doesn't go below 0
        )
        
        return self.repository.update(product_id, updated_product) 