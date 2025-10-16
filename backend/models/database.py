"""
Database Connection and Management
"""
import sqlite3
from typing import Optional
from contextlib import contextmanager


class Database:
    """Database connection manager"""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Threads table
        c.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                thread_id TEXT PRIMARY KEY,
                topic TEXT,
                subject TEXT,
                initiated_by TEXT,
                order_id TEXT,
                product TEXT,
                messages TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Summaries table
        c.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                original_summary TEXT,
                edited_summary TEXT,
                status TEXT DEFAULT 'pending',
                summary_type TEXT,
                crm_context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP,
                approved_by TEXT,
                FOREIGN KEY (thread_id) REFERENCES threads (thread_id)
            )
        ''')
        
        # Audit log table
        c.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                action TEXT,
                user TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        c.execute('CREATE INDEX IF NOT EXISTS idx_threads_order_id ON threads(order_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_summaries_thread_id ON summaries(thread_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_summaries_status ON summaries(status)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_audit_thread_id ON audit_log(thread_id)')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @contextmanager
    def get_db(self):
        """Context manager for database connections"""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

