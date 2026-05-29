import pytest
from sqlalchemy.exc import IntegrityError
from ..models.employee import Employee
# from .conftest import db_session

class TestAnalyticModels:
    def test_employee_creation(self):
        employee = Employee(
            employee_id="35",
            name="Alice",
            department="HR",
            location="New York",
            employment_type="FullTime",
            salary_band="B1"
        )
        assert employee.name == "Alice"
        assert employee.department == "HR"

    def no_test_employee_duplicate_employee_id(self, db_session):
        employee1 = Employee(
            employee_id="20",
            name="Alice",
            department="HR",
            location="New York",
            employment_type="FullTime",
            salary_band="B1"
        )
        employee2 = Employee(
            employee_id="20",
            name="Bob",
            department="IT",
            location="San Francisco",
            employment_type="PartTime",
            salary_band="B2"
        )
        db_session.add(employee1)
        db_session.commit()
        db_session.add(employee2)
        with pytest.raises(IntegrityError):
            db_session.commit()
            # db_session.rollback()
