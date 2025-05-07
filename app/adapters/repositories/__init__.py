from enum import Enum
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.interfaces.product_repository import ProductRepository
from .sql_product_repository import SQLProductRepository
from .nosql_product_repository import NoSQLProductRepository


class RepositoryType(str, Enum):
    SQL = "sql"
    NOSQL = "nosql"


def get_product_repository(
    repository_type: RepositoryType, db_session: Optional[Session] = None
) -> ProductRepository:
    if repository_type == RepositoryType.SQL:
        if not db_session:
            raise ValueError("DB session is required for SQL repository")
        return SQLProductRepository(db_session)
    else:
        return NoSQLProductRepository()
