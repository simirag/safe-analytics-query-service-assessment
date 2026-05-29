from ..models.base import BaseDBModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

class AuditLog(BaseDBModel):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_by = Column(String(100), nullable=True)
    filter = Column(String(100), nullable=True)
    suppression_triggered = Column(Boolean, default=True)
    timestamp = Column(DateTime, server_default=func.now())

    def to_dict(self):
        """Convert the AuditLog instance to a dictionary."""
        return {
            "id": self.id,
            "group_by": self.group_by,
            "filter": self.filter,
            "suppression_triggered": self.suppression_triggered,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }