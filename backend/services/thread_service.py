"""
Thread Business Logic Service
"""
import json
from typing import List, Optional
from models.database import Database
from models.thread import Thread
from models.audit_log import AuditLog


class ThreadService:
    """Business logic for thread operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_threads(self) -> List[Thread]:
        """Get all threads"""
        with self.db.get_db() as conn:
            rows = conn.execute('SELECT * FROM threads ORDER BY created_at DESC').fetchall()
            return [Thread.from_row(row) for row in rows]
    
    def get_thread_by_id(self, thread_id: str) -> Optional[Thread]:
        """Get thread by ID"""
        with self.db.get_db() as conn:
            row = conn.execute(
                'SELECT * FROM threads WHERE thread_id = ?',
                (thread_id,)
            ).fetchone()
            
            if row:
                return Thread.from_row(row)
            return None
    
    def create_thread(self, thread: Thread) -> Thread:
        """Create new thread"""
        with self.db.get_db() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO threads 
                (thread_id, topic, subject, initiated_by, order_id, product, messages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                thread.thread_id,
                thread.topic,
                thread.subject,
                thread.initiated_by,
                thread.order_id,
                thread.product,
                json.dumps(thread.messages)
            ))
            
            # Log the action
            self._log_action(conn, thread.thread_id, 'thread_created', 'system', 
                           f"Thread {thread.thread_id} created")
        
        return thread
    
    def import_threads(self, threads_data: List[dict]) -> tuple[int, int]:
        """Import multiple threads"""
        imported = 0
        total = len(threads_data)
        
        for thread_data in threads_data:
            try:
                thread = Thread.from_dict(thread_data)
                self.create_thread(thread)
                imported += 1
            except Exception as e:
                print(f"Error importing thread {thread_data.get('thread_id')}: {e}")
        
        return imported, total
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete thread"""
        with self.db.get_db() as conn:
            cursor = conn.execute(
                'DELETE FROM threads WHERE thread_id = ?',
                (thread_id,)
            )
            
            if cursor.rowcount > 0:
                self._log_action(conn, thread_id, 'thread_deleted', 'system',
                               f"Thread {thread_id} deleted")
                return True
            return False
    
    def _log_action(self, conn, thread_id: str, action: str, user: str, details: str):
        """Log action to audit log"""
        conn.execute('''
            INSERT INTO audit_log (thread_id, action, user, details)
            VALUES (?, ?, ?, ?)
        ''', (thread_id, action, user, details))

