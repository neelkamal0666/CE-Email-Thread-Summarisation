"""
NLP Service for Summarization
"""
import json
from typing import Dict, Optional
import openai


class NLPService:
    """NLP summarization service with multiple strategies"""
    
    def __init__(self, openai_api_key: str = '', model: str = 'gpt-4',
                 temperature: float = 0.3, max_tokens: int = 500):
        self.openai_api_key = openai_api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def summarize(self, thread_data: Dict) -> Dict:
        """Main summarization method with fallback"""
        # Try OpenAI first if API key is available
        if self.openai_api_key:
            openai_summary = self._summarize_with_openai(thread_data)
            if openai_summary:
                openai_summary['summary_type'] = 'openai'
                return openai_summary
        
        # Fall back to rule-based
        rule_summary = self._summarize_with_rules(thread_data)
        rule_summary['summary_type'] = 'rule_based'
        return rule_summary
    
    def _summarize_with_openai(self, thread_data: Dict) -> Optional[Dict]:
        """Use OpenAI GPT for intelligent summarization"""
        try:
            # Format thread for summarization
            messages_text = ""
            for msg in thread_data['messages']:
                sender = "Customer" if msg['sender'] == 'customer' else "Agent"
                messages_text += f"{sender} ({msg['timestamp']}): {msg['body']}\n\n"
            
            prompt = f"""Analyze this customer service email thread and provide a structured summary.

Thread Information:
- Order ID: {thread_data['order_id']}
- Product: {thread_data['product']}
- Topic: {thread_data['topic']}
- Subject: {thread_data['subject']}

Email Thread:
{messages_text}

Provide a JSON response with:
1. issue_summary: Brief description of the customer's main issue
2. key_actions: List of actions taken or needed
3. resolution_status: Current status (resolved, pending, escalated)
4. sentiment: Customer sentiment (positive, neutral, negative, frustrated)
5. priority: Priority level (low, medium, high, urgent)
6. next_steps: What needs to happen next
7. tags: Relevant tags for categorization

Format as valid JSON."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a customer service summarization assistant. Provide clear, actionable summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            summary_text = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                return json.loads(summary_text)
            except json.JSONDecodeError:
                return {"issue_summary": summary_text}
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def _summarize_with_rules(self, thread_data: Dict) -> Dict:
        """Rule-based summarization as fallback"""
        messages = thread_data['messages']
        
        # Extract key information
        total_messages = len(messages)
        customer_messages = [m for m in messages if m['sender'] == 'customer']
        company_messages = [m for m in messages if m['sender'] == 'company']
        
        # Analyze keywords
        all_text = ' '.join([m['body'].lower() for m in messages])
        
        # Issue detection
        issue_keywords = {
            'damaged': ['damaged', 'broken', 'defective'],
            'delivery': ['delayed', 'late', 'where', 'tracking', 'stuck'],
            'wrong_item': ['wrong', 'color', 'size'],
            'refund': ['refund', 'return', 'credit'],
            'address': ['address', 'reroute']
        }
        
        detected_issues = []
        for issue_type, keywords in issue_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                detected_issues.append(issue_type.replace('_', ' '))
        
        # Sentiment analysis (simple)
        negative_words = ['broken', 'wrong', 'delayed', 'stuck', 'lost', 'issue', 'problem']
        positive_words = ['resolved', 'thanks', 'appreciate', 'approve']
        
        neg_count = sum(1 for word in negative_words if word in all_text)
        pos_count = sum(1 for word in positive_words if word in all_text)
        
        # Status determination
        if 'resolved' in all_text:
            status = 'resolved'
        elif total_messages > 5:
            status = 'escalated'
        else:
            status = 'pending'
        
        # Sentiment
        if neg_count > pos_count * 2:
            sentiment = 'frustrated'
        elif neg_count > pos_count:
            sentiment = 'negative'
        elif pos_count > neg_count:
            sentiment = 'positive'
        else:
            sentiment = 'neutral'
        
        # Priority
        if 'urgent' in all_text or total_messages > 6:
            priority = 'urgent'
        elif total_messages > 4 or detected_issues:
            priority = 'high'
        else:
            priority = 'medium'
        
        return {
            "issue_summary": f"Customer contacted regarding {thread_data['product']} (Order {thread_data['order_id']}). Issues: {', '.join(detected_issues) if detected_issues else thread_data['topic']}.",
            "key_actions": [
                f"Total messages exchanged: {total_messages}",
                f"Customer messages: {len(customer_messages)}",
                f"Agent responses: {len(company_messages)}"
            ],
            "resolution_status": status,
            "sentiment": sentiment,
            "priority": priority,
            "next_steps": "Review thread and take appropriate action" if status != 'resolved' else "Thread appears resolved",
            "tags": detected_issues
        }

