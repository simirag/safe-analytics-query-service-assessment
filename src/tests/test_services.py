import pytest
from unittest.mock import patch
from ..services.analytics import AnalyticsService
from ..core.exceptions import InvalidQueryException
from ..config import settings

class TestAnalyticsService:

    def test_get_employee_statistics_valid(self, db_session):
        with patch('src.config.settings.SUPPRESSED', 2):
            service = AnalyticsService(db_session)
            stats = service.get_employee_statistics(group_by="department", filter_data={"location": "San Francisco"})
            assert stats == {"IT": 3}

    def test_get_employee_statistics_no_results(self, db_session):
        service = AnalyticsService(db_session)
        stats = service.get_employee_statistics(group_by="department", filter_data={"location": "Nonexistent"})
        assert stats == {}

    def test_get_employee_statistics_invalid_group_by(self, db_session):
        service = AnalyticsService(db_session)
        try:
            service.get_employee_statistics(group_by="invalid_field", filter_data={"location": "San Francisco"})
            assert False, "Expected InvalidQueryException"
        except InvalidQueryException as e:
            assert str(e) == "400: Invalid group_by value: invalid_field"

    def test_get_employee_statistics_invalid_filter(self, db_session):
        service = AnalyticsService(db_session)
        try:
            service.get_employee_statistics(group_by="department", filter_data={"invalid_field": "value"})
            assert False, "Expected InvalidQueryException"
        except InvalidQueryException as e:
            assert str(e) == "400: Invalid filter key: invalid_field value: value"