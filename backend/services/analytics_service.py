"""
Analytics Business Logic Service
"""
from typing import Dict
from models.database import Database


class AnalyticsService:
    """Business logic for analytics operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_dashboard_analytics(self) -> Dict:
        """Get dashboard analytics"""
        with self.db.get_db() as conn:
            # Summary statistics
            total_threads = conn.execute(
                'SELECT COUNT(*) as count FROM threads'
            ).fetchone()['count']
            
            total_summaries = conn.execute(
                'SELECT COUNT(*) as count FROM summaries'
            ).fetchone()['count']
            
            pending_summaries = conn.execute(
                'SELECT COUNT(*) as count FROM summaries WHERE status = "pending" OR status = "edited"'
            ).fetchone()['count']
            
            approved_summaries = conn.execute(
                'SELECT COUNT(*) as count FROM summaries WHERE status = "approved"'
            ).fetchone()['count']
            
            # Calculate approval rate
            approval_rate = 0
            if total_summaries > 0:
                approval_rate = (approved_summaries / total_summaries) * 100
            
            return {
                "total_threads": total_threads,
                "total_summaries": total_summaries,
                "pending_summaries": pending_summaries,
                "approved_summaries": approved_summaries,
                "approval_rate": round(approval_rate, 2)
            }
    
    def get_summary_stats_by_type(self) -> Dict:
        """Get summary statistics by type"""
        with self.db.get_db() as conn:
            rows = conn.execute('''
                SELECT summary_type, COUNT(*) as count
                FROM summaries
                GROUP BY summary_type
            ''').fetchall()
            
            return {row['summary_type']: row['count'] for row in rows}
    
    def get_summary_stats_by_status(self) -> Dict:
        """Get summary statistics by status"""
        with self.db.get_db() as conn:
            rows = conn.execute('''
                SELECT status, COUNT(*) as count
                FROM summaries
                GROUP BY status
            ''').fetchall()
            
            return {row['status']: row['count'] for row in rows}

