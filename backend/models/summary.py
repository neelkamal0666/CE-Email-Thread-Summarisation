"""
Summary Model
"""
import json
from typing import Dict, Optional
from datetime import datetime


class Summary:
    """Summary model"""
    
    def __init__(
        self,
        thread_id: str,
        original_summary: Dict,
        edited_summary: Optional[Dict] = None,
        status: str = 'pending',
        summary_type: str = 'unknown',
        crm_context: Optional[Dict] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        approved_at: Optional[str] = None,
        approved_by: Optional[str] = None
    ):
        self.id = id
        self.thread_id = thread_id
        self.original_summary = original_summary
        self.edited_summary = edited_summary or original_summary
        self.status = status
        self.summary_type = summary_type
        self.crm_context = crm_context or {}
        self.created_at = created_at or datetime.now().isoformat()
        self.approved_at = approved_at
        self.approved_by = approved_by
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'original_summary': self.original_summary,
            'edited_summary': self.edited_summary,
            'status': self.status,
            'summary_type': self.summary_type,
            'crm_context': self.crm_context,
            'created_at': self.created_at,
            'approved_at': self.approved_at,
            'approved_by': self.approved_by
        }
    
    @classmethod
    def from_row(cls, row) -> 'Summary':
        """Create from database row"""
        return cls(
            id=row['id'],
            thread_id=row['thread_id'],
            original_summary=json.loads(row['original_summary']),
            edited_summary=json.loads(row['edited_summary']),
            status=row['status'],
            summary_type=row['summary_type'],
            crm_context=json.loads(row['crm_context']) if row['crm_context'] else None,
            created_at=row['created_at'],
            approved_at=row['approved_at'],
            approved_by=row['approved_by']
        )
    
    def approve(self, user: str):
        """Approve summary"""
        self.status = 'approved'
        self.approved_at = datetime.now().isoformat()
        self.approved_by = user
    
    def reject(self):
        """Reject summary"""
        self.status = 'rejected'
    
    def edit(self, edited_summary: Dict):
        """Edit summary"""
        self.edited_summary = edited_summary
        self.status = 'edited'

