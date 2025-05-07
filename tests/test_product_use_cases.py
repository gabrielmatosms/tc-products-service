import pytest
from unittest.mock import MagicMock

from app.application.use_cases.product_use_cases import ProductUseCases
from app.domain.entities.product import Product, ProductDb, ProductCategory
from app.domain.interfaces.product_repository import ProductRepository


class TestProductUseCases:
    def setup_method(self):
        self.mock_repo = MagicMock(spec=ProductRepository)
        self.use_cases = ProductUseCases(self.mock_repo)

    def test_get_all_products(self):
        products = [
            ProductDb(
                id=1, name="Burger", description="Tasty burger", 
                category=ProductCategory.MAIN_ITEM, price=15.99, quantity=10,
                created_at=None, updated_at=None
            ),
            ProductDb(
                id=2, name="Fries", description="Crispy fries", 
                category=ProductCategory.SIDE, price=5.99, quantity=20,
                created_at=None, updated_at=None
            )
        ]
        self.mock_repo.get_all.return_value = products

        result = self.use_cases.get_all_products()

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        self.mock_repo.get_all.assert_called_once()

    def test_get_product_by_id(self):
        product = ProductDb(
            id=1, name="Burger", description="Tasty burger", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=10,
            created_at=None, updated_at=None
        )
        self.mock_repo.get_by_id.return_value = product

        result = self.use_cases.get_product_by_id(1)

        assert result.id == 1
        assert result.name == "Burger"
        self.mock_repo.get_by_id.assert_called_once_with(1)
        
    def test_get_product_by_id_not_found(self):
        self.mock_repo.get_by_id.return_value = None

        result = self.use_cases.get_product_by_id(999)

        assert result is None
        self.mock_repo.get_by_id.assert_called_once_with(999)
        
    def test_create_product(self):
        product = Product(
            name="New Product", description="Brand new", 
            category=ProductCategory.DRINK, price=3.99, quantity=50
        )
        created_product = ProductDb(
            id=3, name="New Product", description="Brand new", 
            category=ProductCategory.DRINK, price=3.99, quantity=50,
            created_at=None, updated_at=None
        )
        self.mock_repo.create.return_value = created_product

        result = self.use_cases.create_product(product)

        assert result.id == 3
        assert result.name == "New Product"
        self.mock_repo.create.assert_called_once_with(product)
        
    def test_update_product(self):
        product_id = 1
        product = Product(
            name="Updated Product", description="Updated description", 
            category=ProductCategory.MAIN_ITEM, price=16.99, quantity=5
        )
        existing = ProductDb(
            id=product_id, name="Old Name", description="Old description", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=10,
            created_at=None, updated_at=None
        )
        updated = ProductDb(
            id=product_id, name="Updated Product", description="Updated description", 
            category=ProductCategory.MAIN_ITEM, price=16.99, quantity=5,
            created_at=None, updated_at=None
        )
        self.mock_repo.get_by_id.return_value = existing
        self.mock_repo.update.return_value = updated

        result = self.use_cases.update_product(product_id, product)

        assert result.id == product_id
        assert result.name == "Updated Product"
        assert result.price == 16.99
        self.mock_repo.get_by_id.assert_called_once_with(product_id)
        self.mock_repo.update.assert_called_once_with(product_id, product)
        
    def test_update_product_not_found(self):
        product_id = 999
        product = Product(
            name="Updated Product", description="Updated description", 
            category=ProductCategory.MAIN_ITEM, price=16.99, quantity=5
        )
        self.mock_repo.get_by_id.return_value = None

        result = self.use_cases.update_product(product_id, product)

        assert result is None
        self.mock_repo.get_by_id.assert_called_once_with(product_id)
        self.mock_repo.update.assert_not_called()
        
    def test_delete_product(self):
        product_id = 1
        self.mock_repo.delete.return_value = True

        result = self.use_cases.delete_product(product_id)

        assert result is True
        self.mock_repo.delete.assert_called_once_with(product_id)
        
    def test_update_product_quantity(self):
        product_id = 1
        quantity_change = -2
        
        existing = ProductDb(
            id=product_id, name="Product", description="Description", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=10,
            created_at=None, updated_at=None
        )
        
        updated = ProductDb(
            id=product_id, name="Product", description="Description", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=8,
            created_at=None, updated_at=None
        )
        
        self.mock_repo.get_by_id.return_value = existing
        self.mock_repo.update.return_value = updated
        
        result = self.use_cases.update_product_quantity(product_id, quantity_change)
        
        assert result.quantity == 8
        self.mock_repo.get_by_id.assert_called_once_with(product_id)
        self.mock_repo.update.assert_called_once()
        
    def test_update_product_quantity_not_below_zero(self):
        product_id = 1
        quantity_change = -15
        
        existing = ProductDb(
            id=product_id, name="Product", description="Description", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=10,
            created_at=None, updated_at=None
        )
        
        updated = ProductDb(
            id=product_id, name="Product", description="Description", 
            category=ProductCategory.MAIN_ITEM, price=15.99, quantity=0,
            created_at=None, updated_at=None
        )
        
        self.mock_repo.get_by_id.return_value = existing
        self.mock_repo.update.return_value = updated
        
        result = self.use_cases.update_product_quantity(product_id, quantity_change)
        
        assert result.quantity == 0
        self.mock_repo.get_by_id.assert_called_once_with(product_id)
        self.mock_repo.update.assert_called_once() 