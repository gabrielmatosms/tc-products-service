import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.adapters.models.sql.base import Base
from app.adapters.models.sql.session import get_db

# Configuração do banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Usa uma conexão compartilhada para o teste inteiro
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(bind=connection)
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_get_product(client):
    # Cria produto
    product = {
        "name": "Test Burger",
        "description": "Delicious test burger",
        "category": "Main Item",
        "price": 10.5,
        "quantity": 5
    }
    response = client.post("/api/v1/products/", json=product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product["name"]
    product_id = data["id"]

    # Busca todos
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Busca por id
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

def test_update_product(client):
    # Cria produto
    product = {
        "name": "Test Fries",
        "description": "Test fries",
        "category": "Side",
        "price": 4.0,
        "quantity": 10
    }
    response = client.post("/api/v1/products/", json=product)
    product_id = response.json()["id"]

    # Atualiza produto
    updated = product.copy()
    updated["name"] = "Updated Fries"
    updated["price"] = 5.0
    response = client.put(f"/api/v1/products/{product_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Fries"
    assert response.json()["price"] == 5.0

def test_update_quantity(client):
    # Cria produto
    product = {
        "name": "Test Drink",
        "description": "Test drink",
        "category": "Drink",
        "price": 2.5,
        "quantity": 8
    }
    response = client.post("/api/v1/products/", json=product)
    product_id = response.json()["id"]

    # Atualiza quantidade
    response = client.patch(f"/api/v1/products/{product_id}/quantity/-3")
    assert response.status_code == 200
    assert response.json()["quantity"] == 5

def test_delete_product(client):
    # Cria produto
    product = {
        "name": "Test Dessert",
        "description": "Test dessert",
        "category": "Dessert",
        "price": 6.0,
        "quantity": 3
    }
    response = client.post("/api/v1/products/", json=product)
    product_id = response.json()["id"]

    # Deleta produto
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 200 or response.status_code == 204

    # Verifica que não existe mais
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 404 