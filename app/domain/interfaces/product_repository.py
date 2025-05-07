from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product, ProductDb


class ProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ProductDb]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[ProductDb]:
        pass

    @abstractmethod
    def create(self, product: Product) -> ProductDb:
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product) -> Optional[ProductDb]:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass 