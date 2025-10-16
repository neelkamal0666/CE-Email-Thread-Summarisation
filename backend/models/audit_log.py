"""
Audit Log Model
"""
from typing import Optional
from datetime import datetime


class AuditLog:
    """Audit log entry model"""
    
    def __init__(
        self,
        thread_id: str,
        action: str,
        user: str,
        details: str,
        id: Optional[int] = None,
        timestamp: Optional[str] = None
    ):
        self.id = id
        self.thread_id = thread_id
        self.action = action
        self.user = user
        self.details = details
        self.timestamp = timestamp or datetime.now().isoformat()
    
    @classmethod
    def from_row(cls, row) -> 'AuditLog':
        """Create from database row"""
        return cls(
            id=row['id'],
            thread_id=row['thread_id'],
            action=row['action'],
            user=row['user'],
            details=row['details'],
            timestamp=row['timestamp']
        )

