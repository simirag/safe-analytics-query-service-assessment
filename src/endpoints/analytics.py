from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Any
from typing import Annotated
from fastapi import Body

from ..database import get_db
from ..config import settings
from ..schemas.analytics import AnalyticsQuery, EmployeeStatistics
from ..services.analytics import AnalyticsService
from ..core.exceptions import InvalidQueryException
from ..core.logger import get_logger
from ..services.audit_service import AuditService

router = APIRouter()
logger = get_logger(__name__)

@router.post("/query")
async def query_analytics(
    analytics_query: AnalyticsQuery,
    db: Session = Depends(get_db)
) -> Any:
    """
    Employee analytics query.
    Args:
    - `group_by`: Optional field to specify the attribute to group by (e.g., department, location).
    - `filter`: Optional dictionary to specify filtering criteria (e.g., {"department": "HR"}).
    Returns: 
        dictionary with the aggregated statistics based on the provided query parameters.
    """
    try:
        service = AnalyticsService(db)
        logger.info(f"Received analytics query: group_by={analytics_query.group_by}, filter={analytics_query.filter}")
        stats = service.get_employee_statistics(
            group_by=analytics_query.group_by,
            filter_data=analytics_query.filter
        )
        return stats
    except InvalidQueryException as e:
        logger.error(f"Invalid query: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get("/audit-log")
async def get_audit_log(db: Session = Depends(get_db)):
    service = AuditService(db)
    logs = service.get_audit_logs()
    return logs
