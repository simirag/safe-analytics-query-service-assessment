from sqlalchemy import Column, String, Integer

from .base import BaseDBModel

class Employee(BaseDBModel):
    __tablename__ = "employees"

    employee_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100))
    department = Column(String(100), index=True)
    location = Column(String(100), index=True)
    employment_type = Column(String(100), index=True)
    salary_band = Column(String(100), index=True)
    

