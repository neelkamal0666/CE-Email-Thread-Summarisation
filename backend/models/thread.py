"""
Thread Model
"""
import json
from typing import List, Dict, Optional
from datetime import datetime


class Thread:
    """Email thread model"""
    
    def __init__(
        self,
        thread_id: str,
        topic: str,
        subject: str,
        initiated_by: str,
        order_id: str,
        product: str,
        messages: List[Dict],
        created_at: Optional[str] = None
    ):
        self.thread_id = thread_id
        self.topic = topic
        self.subject = subject
        self.initiated_by = initiated_by
        self.order_id = order_id
        self.product = product
        self.messages = messages
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'thread_id': self.thread_id,
            'topic': self.topic,
            'subject': self.subject,
            'initiated_by': self.initiated_by,
            'order_id': self.order_id,
            'product': self.product,
            'messages': self.messages,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Thread':
        """Create from dictionary"""
        return cls(
            thread_id=data['thread_id'],
            topic=data['topic'],
            subject=data['subject'],
            initiated_by=data['initiated_by'],
            order_id=data['order_id'],
            product=data['product'],
            messages=data['messages'],
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_row(cls, row) -> 'Thread':
        """Create from database row"""
        return cls(
            thread_id=row['thread_id'],
            topic=row['topic'],
            subject=row['subject'],
            initiated_by=row['initiated_by'],
            order_id=row['order_id'],
            product=row['product'],
            messages=json.loads(row['messages']),
            created_at=row['created_at']
        )

