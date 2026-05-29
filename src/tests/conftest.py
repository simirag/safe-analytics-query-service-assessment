import pytest
import os
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.database import get_db, Base
from src.main import app
from src.config import settings
from src.models.employee import Employee

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
settings.SUPPRESSED = 2

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_session():
    """Create a fresh database for testing."""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def mock_setings():
    with patch('src.config.settings') as mock_settings:
        mock_settings.SUPPRESSED = 2
        yield mock_settings
    
@pytest.fixture(scope="session")
def analytic_employee_data(db_session):
    """Insert test employee data for analytics tests."""
    employees = [
        Employee(id=1, employee_id="1", name="Alice", department="HR", location="New York", employment_type="FullTime", salary_band="B1"),
        Employee(id=2, employee_id="2", name="Bob", department="HR", location="New York", employment_type="FullTime", salary_band="B1"),
        Employee(id=3, employee_id="3", name="Charlie", department="IT", location="San Francisco", employment_type="PartTime", salary_band="B2"),
        Employee(id=4, employee_id="4", name="David", department="IT", location="San Francisco", employment_type="PartTime", salary_band="B2"),
        Employee(id=5, employee_id="5", name="Eve", department="IT", location="San Francisco", employment_type="FullTime", salary_band="B2"),
        Employee(id=6, employee_id="6", name="Frank", department="Finance", location="Chicago", employment_type="FullTime", salary_band="B3")
    ]
    db_session.add_all(employees)
    db_session.commit()
    # db_session.refresh(employees)
    return employees

