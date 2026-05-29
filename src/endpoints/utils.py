from fastapi import APIRouter, Depends

from ..database import get_db
from ..core.utils import load_csv_data
from ..config import settings
router = APIRouter()

@router.post("/load-test-data")
async def load_test_data(db=Depends(get_db)):
    if settings.ENVIRONMENT != "development":
        return {"message": "Test data loading is only allowed in development environment"}
    file_path = settings.TEST_DATA_FILE
    load_csv_data(file_path, db)
    return {"message": "Test data loaded successfully"}

