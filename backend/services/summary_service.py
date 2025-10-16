"""
Summary Business Logic Service
"""
import json
from typing import List, Optional, Dict
from datetime import datetime
from models.database import Database
from models.summary import Summary
from models.thread import Thread


class SummaryService:
    """Business logic for summary operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_summaries(self, status: Optional[str] = None) -> List[Summary]:
        """Get all summaries, optionally filtered by status"""
        with self.db.get_db() as conn:
            if status:
                rows = conn.execute(
                    'SELECT * FROM summaries WHERE status = ? ORDER BY created_at DESC',
                    (status,)
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT * FROM summaries ORDER BY created_at DESC'
                ).fetchall()
            
            return [Summary.from_row(row) for row in rows]
    
    def get_summary_by_id(self, summary_id: int) -> Optional[Summary]:
        """Get summary by ID"""
        with self.db.get_db() as conn:
            row = conn.execute(
                'SELECT * FROM summaries WHERE id = ?',
                (summary_id,)
            ).fetchone()
            
            if row:
                return Summary.from_row(row)
            return None
    
    def create_summary(self, summary: Summary) -> int:
        """Create new summary"""
        with self.db.get_db() as conn:
            cursor = conn.execute('''
                INSERT INTO summaries 
                (thread_id, original_summary, edited_summary, status, summary_type, crm_context)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                summary.thread_id,
                json.dumps(summary.original_summary),
                json.dumps(summary.edited_summary),
                summary.status,
                summary.summary_type,
                json.dumps(summary.crm_context)
            ))
            
            summary_id = cursor.lastrowid
            
            # Log the action
            self._log_action(conn, summary.thread_id, 'summary_generated', 'system',
                           f"Summary ID: {summary_id}")
            
            return summary_id
    
    def update_summary(self, summary_id: int, edited_summary: Dict, user: str) -> bool:
        """Update summary with edits"""
        with self.db.get_db() as conn:
            cursor = conn.execute('''
                UPDATE summaries 
                SET edited_summary = ?, status = 'edited'
                WHERE id = ?
            ''', (json.dumps(edited_summary), summary_id))
            
            if cursor.rowcount > 0:
                # Get thread_id for audit
                row = conn.execute(
                    'SELECT thread_id FROM summaries WHERE id = ?',
                    (summary_id,)
                ).fetchone()
                
                if row:
                    self._log_action(conn, row['thread_id'], 'summary_edited', user,
                                   f"Summary ID: {summary_id}")
                return True
            return False
    
    def approve_summary(self, summary_id: int, user: str) -> bool:
        """Approve summary"""
        with self.db.get_db() as conn:
            cursor = conn.execute('''
                UPDATE summaries 
                SET status = 'approved', approved_at = ?, approved_by = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), user, summary_id))
            
            if cursor.rowcount > 0:
                # Get thread_id for audit
                row = conn.execute(
                    'SELECT thread_id FROM summaries WHERE id = ?',
                    (summary_id,)
                ).fetchone()
                
                if row:
                    self._log_action(conn, row['thread_id'], 'summary_approved', user,
                                   f"Summary ID: {summary_id}")
                return True
            return False
    
    def reject_summary(self, summary_id: int, user: str, reason: str = '') -> bool:
        """Reject summary"""
        with self.db.get_db() as conn:
            cursor = conn.execute('''
                UPDATE summaries 
                SET status = 'rejected'
                WHERE id = ?
            ''', (summary_id,))
            
            if cursor.rowcount > 0:
                # Get thread_id for audit
                row = conn.execute(
                    'SELECT thread_id FROM summaries WHERE id = ?',
                    (summary_id,)
                ).fetchone()
                
                if row:
                    self._log_action(conn, row['thread_id'], 'summary_rejected', user,
                                   f"Summary ID: {summary_id}, Reason: {reason}")
                return True
            return False
    
    def get_export_data(self, summary_id: int) -> Optional[Dict]:
        """Get export data for approved summary"""
        with self.db.get_db() as conn:
            row = conn.execute('''
                SELECT s.*, t.* 
                FROM summaries s
                JOIN threads t ON s.thread_id = t.thread_id
                WHERE s.id = ?
            ''', (summary_id,)).fetchone()
            
            if not row:
                return None
            
            if row['status'] != 'approved':
                return None
            
            return {
                "thread_id": row['thread_id'],
                "order_id": row['order_id'],
                "product": row['product'],
                "topic": row['topic'],
                "summary": json.loads(row['edited_summary']),
                "crm_context": json.loads(row['crm_context']) if row['crm_context'] else None,
                "approved_by": row['approved_by'],
                "approved_at": row['approved_at'],
                "export_timestamp": datetime.now().isoformat()
            }
    
    def _log_action(self, conn, thread_id: str, action: str, user: str, details: str):
        """Log action to audit log"""
        conn.execute('''
            INSERT INTO audit_log (thread_id, action, user, details)
            VALUES (?, ?, ?, ?)
        ''', (thread_id, action, user, details))

