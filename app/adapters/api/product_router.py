from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.adapters.models.sql.session import get_db
from app.adapters.repositories import RepositoryType, get_product_repository
from app.application.use_cases.product_use_cases import ProductUseCases
from app.domain.entities.product import Product, ProductDb, ProductCategory

router = APIRouter()

# Helper function to get product use cases with SQL repository
def get_product_use_cases(db: Session = Depends(get_db)) -> ProductUseCases:
    repository = get_product_repository(RepositoryType.SQL, db)
    return ProductUseCases(repository)


@router.get("/", response_model=List[ProductDb])
def get_all_products(use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return use_cases.get_all_products()


@router.get("/categories", response_model=List[str])
def get_categories():
    return [category.value for category in ProductCategory]


@router.get("/{product_id}", response_model=ProductDb)
def get_product(product_id: int, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    product = use_cases.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


@router.post("/", response_model=ProductDb, status_code=status.HTTP_201_CREATED)
def create_product(product: Product, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return use_cases.create_product(product)


@router.put("/{product_id}", response_model=ProductDb)
def update_product(
    product_id: int, product: Product, use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    updated_product = use_cases.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    deleted = use_cases.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )


@router.patch("/{product_id}/quantity/{change}", response_model=ProductDb)
def update_quantity(
    product_id: int, change: int, use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    """
    Update product quantity by adding the change amount (use negative for reduction)
    """
    updated_product = use_cases.update_product_quantity(product_id, change)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return updated_product 