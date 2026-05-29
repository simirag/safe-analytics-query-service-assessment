from pydantic import BaseModel
from enum import Enum

class GroupByOption(str, Enum):
    """Enum for group by options."""

    DEPARTMENT = "department"
    LOCATION = "location"
    EMPLOYMENT_TYPE = "employment_type"
    SALARY_BAND = "salary_band"
    

class FilterOption(str, Enum):
    """Enum for filter options."""

    DEPARTMENT = "department"
    LOCATION = "location"
    EMPLOYMENT_TYPE = "employment_type"
    SALARY_BAND = "salary_band"
    NAME = "name"

class AnalyticsQuery(BaseModel):
    """Pydantic model for an analytics query."""

    group_by: str
    filter: dict[str, str] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "group_by": "department",
                    "filter": {"location": "London"}
                },
                {
                    "group_by": "location",
                    "filter": {"location": "London", "department": "Engineering"}
                }
            ]
        }
    }

class EmployeeStatistics(BaseModel):
    """Pydantic model for employee statistics response."""

    data: dict[str, int]
    model_config = {"embed_data": False}

