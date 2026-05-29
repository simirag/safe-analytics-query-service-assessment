import json
from sqlalchemy import func
from ..models.employee import Employee
from ..schemas.analytics import AnalyticsQuery, GroupByOption, FilterOption
from ..core.exceptions import InvalidQueryException
from .audit_service import AuditService
from ..config import settings


class AnalyticsService:
    """Service class for analytics operations."""
    def __init__(self, db):
        self.db = db
        self.audit_service = AuditService(db)

    def get_employee_statistics(self, group_by, filter_data):
        """Get aggregated employee statistics.
        Args:
            group_by (str | None): The attribute to group by (e.g., department, location).
            filter_data (dict[str, str] | None): The filtering criteria (e.g., {"department": "HR"}).
        Returns:
            List of tuples containing the grouped attribute and its count.
        """
        
        query = self.db.query(Employee)
        filters = []
        if filter_data is not None:
            for key, value in filter_data.items():
                if key not in FilterOption.__members__.values():
                    raise InvalidQueryException(f"Invalid filter key: {key} value: {value}")
                filters.append(getattr(Employee, key) == value)

        if group_by is not None:
            if group_by not in GroupByOption.__members__.values():
                raise InvalidQueryException(f"Invalid group_by value: {group_by}")
            query = self.db.query(getattr(Employee, group_by), func.count(Employee.id).label("t_count"))
            query = query.group_by(getattr(Employee, group_by))

        query = query.filter(*filters)
        stats = query.all()

        result = {}
        suppressed = "False"
        for stat in stats:
            result[stat[0]] = stat[1]
            # stat[1] if stat[1] > settings.SUPPRESSED else "Suppressed"
            if stat[1] <= settings.SUPPRESSED:
                result[stat[0]] = "Suppressed"
                suppressed = "True"

        self.audit_service.log_audit(
            action="query_analytics",
            group_by=group_by,
            filter=json.dumps(filter_data) if filter_data else None,
            suppression_triggered=suppressed
        )
        return result