from ..models.base import BaseDBModel
from sqlalchemy import Column, Integer, String, DateTime, func

class AuditLog(BaseDBModel):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action = Column(String(100), nullable=False)
    group_by = Column(String(100), nullable=True)
    filter = Column(String(100), nullable=True)
    suppression_triggered = Column(String(50), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())