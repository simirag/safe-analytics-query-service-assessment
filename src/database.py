from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for getting database session."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if settings.ENVIRONMENT == "development" and not settings.TEST_DATA_LOADED:
            from .scripts.init_db_data import load_csv_data
            from .models.employee import Employee
            load_csv_data(Employee, 'data/employees.csv')
            settings.TEST_DATA_LOADED = True
        yield db
    finally:
        db.close()

