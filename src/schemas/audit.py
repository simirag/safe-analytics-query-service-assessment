from pydantic import BaseModel

class AuditLogSchema(BaseModel):
    """Pydantic model for audit log entries."""

    group_by: str | None = None
    filter: str | None = None
    suppression_triggered: bool
    timestamp: str
