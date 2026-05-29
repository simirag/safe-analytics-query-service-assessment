from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings for the Safe Analytics Query Service Assessment."""
    
    # Application
    DEBUG: bool = True
    PROJECT_NAME: str = "Safe Analytics Query Service Assessment"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/analytics_db"
    DATABASE_URL: str = "sqlite:///./analytics.db"
    SUPPRESSED: int = 3
    ENVIRONMENT: str = "development"
    TEST_DATA_LOADED: bool = False
    TEST_DATA_FILE: str = f"{Path(__file__).parent.parent}/data/employees.csv"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }

def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

settings = get_settings()