from ..models.audit import AuditLog
class AuditService:
    def __init__(self, db_session):
        self.db_session = db_session

    def log_audit(self, action, group_by=None, filter=None, suppression_triggered=None):
        audit_log = AuditLog(
            action=action,
            group_by=group_by,
            filter=filter,
            suppression_triggered=suppression_triggered
        )
        self.db_session.add(audit_log)
        self.db_session.commit()
    
    def get_audit_logs(self, limit=100):
        return self.db_session.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
