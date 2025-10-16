#!/usr/bin/env python3
"""
Simple API test script to verify backend functionality
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Health check passed: {data['status']}")
    print(f"  NLP Method: {data['nlp_method']}")
    return True

def test_import_threads():
    """Test importing threads"""
    print("\nTesting thread import...")
    
    # Load dataset
    with open('ce_exercise_threads UPDATED.txt', 'r') as f:
        data = json.load(f)
    
    response = requests.post(f"{API_BASE}/threads/import", json=data)
    assert response.status_code == 200
    result = response.json()
    print(f"✓ Imported {result['imported']} threads")
    return result['imported']

def test_get_threads():
    """Test retrieving threads"""
    print("\nTesting thread retrieval...")
    response = requests.get(f"{API_BASE}/threads")
    assert response.status_code == 200
    threads = response.json()
    print(f"✓ Retrieved {len(threads)} threads")
    return threads

def test_summarize_thread(thread_id):
    """Test summarization"""
    print(f"\nTesting summarization for {thread_id}...")
    response = requests.post(f"{API_BASE}/threads/{thread_id}/summarize")
    assert response.status_code == 200
    result = response.json()
    print(f"✓ Summary generated (ID: {result['summary_id']})")
    print(f"  Summary type: {result['summary']['summary_type']}")
    return result['summary_id']

def test_get_summaries():
    """Test retrieving summaries"""
    print("\nTesting summary retrieval...")
    response = requests.get(f"{API_BASE}/summaries")
    assert response.status_code == 200
    summaries = response.json()
    print(f"✓ Retrieved {len(summaries)} summaries")
    return summaries

def test_edit_summary(summary_id):
    """Test editing summary"""
    print(f"\nTesting summary edit for ID {summary_id}...")
    
    # Get current summary
    response = requests.get(f"{API_BASE}/summaries/{summary_id}")
    current = response.json()
    
    # Edit it
    edited = current['edited_summary'].copy()
    edited['issue_summary'] = "EDITED: " + edited['issue_summary']
    
    response = requests.put(
        f"{API_BASE}/summaries/{summary_id}/edit",
        json={"edited_summary": edited, "user": "Test User"}
    )
    assert response.status_code == 200
    print(f"✓ Summary edited successfully")
    return True

def test_approve_summary(summary_id):
    """Test approving summary"""
    print(f"\nTesting summary approval for ID {summary_id}...")
    response = requests.post(
        f"{API_BASE}/summaries/{summary_id}/approve",
        json={"user": "Test User"}
    )
    assert response.status_code == 200
    print(f"✓ Summary approved successfully")
    return True

def test_export_summary(summary_id):
    """Test exporting summary"""
    print(f"\nTesting summary export for ID {summary_id}...")
    response = requests.get(f"{API_BASE}/export/{summary_id}")
    assert response.status_code == 200
    export_data = response.json()
    print(f"✓ Summary exported successfully")
    print(f"  Thread ID: {export_data['thread_id']}")
    print(f"  Order ID: {export_data['order_id']}")
    return export_data

def test_analytics():
    """Test analytics endpoint"""
    print("\nTesting analytics...")
    response = requests.get(f"{API_BASE}/analytics")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Analytics retrieved:")
    print(f"  Total threads: {data['total_threads']}")
    print(f"  Total summaries: {data['total_summaries']}")
    print(f"  Pending: {data['pending_summaries']}")
    print(f"  Approved: {data['approved_summaries']}")
    print(f"  Approval rate: {data['approval_rate']:.1f}%")
    return data

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("CE Email Summarization API Test Suite")
    print("=" * 60)
    
    try:
        # Health check
        test_health()
        
        # Import threads
        count = test_import_threads()
        
        # Get threads
        threads = test_get_threads()
        assert len(threads) == count
        
        # Summarize first thread
        thread_id = threads[0]['thread_id']
        summary_id = test_summarize_thread(thread_id)
        
        # Wait a moment for processing
        time.sleep(1)
        
        # Get summaries
        summaries = test_get_summaries()
        assert len(summaries) > 0
        
        # Edit summary
        test_edit_summary(summary_id)
        
        # Approve summary
        test_approve_summary(summary_id)
        
        # Export summary
        export_data = test_export_summary(summary_id)
        
        # Check analytics
        analytics = test_analytics()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API. Is the backend running?")
        print("  Start with: cd backend && python3 app.py")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

