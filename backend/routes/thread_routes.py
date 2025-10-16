"""
Thread API Routes
"""
from flask import Blueprint, request, jsonify, current_app

thread_bp = Blueprint('threads', __name__)


@thread_bp.route('/import', methods=['POST'])
def import_threads():
    """Import threads from JSON"""
    thread_service = current_app.thread_service
    
    try:
        data = request.json
        threads = data.get('threads', [])
        
        imported, total = thread_service.import_threads(threads)
        
        return jsonify({
            "success": True,
            "imported": imported,
            "total": total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@thread_bp.route('', methods=['GET'])
def get_threads():
    """Get all threads"""
    thread_service = current_app.thread_service
    
    threads = thread_service.get_all_threads()
    return jsonify([thread.to_dict() for thread in threads])


@thread_bp.route('/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    """Get specific thread"""
    thread_service = current_app.thread_service
    
    thread = thread_service.get_thread_by_id(thread_id)
    if not thread:
        return jsonify({"error": "Thread not found"}), 404
    
    return jsonify(thread.to_dict())


@thread_bp.route('/<thread_id>/summarize', methods=['POST'])
def summarize_thread(thread_id):
    """Generate summary for a thread"""
    thread_service = current_app.thread_service
    summary_service = current_app.summary_service
    nlp_service = current_app.nlp_service
    
    try:
        # Get thread data
        thread = thread_service.get_thread_by_id(thread_id)
        if not thread:
            return jsonify({"error": "Thread not found"}), 404
        
        # Generate summary
        summary_data = nlp_service.summarize(thread.to_dict())
        
        # Add CRM context
        from models.summary import Summary
        crm_context = {
            "order_id": thread.order_id,
            "product": thread.product,
            "customer_lifetime_value": "N/A",
            "previous_interactions": 0,
            "order_value": "N/A"
        }
        
        # Create summary object
        summary = Summary(
            thread_id=thread_id,
            original_summary=summary_data,
            edited_summary=summary_data,
            status='pending',
            summary_type=summary_data.get('summary_type', 'unknown'),
            crm_context=crm_context
        )
        
        # Save summary
        summary_id = summary_service.create_summary(summary)
        summary.id = summary_id
        
        return jsonify({
            "success": True,
            "summary_id": summary_id,
            "summary": summary_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@thread_bp.route('/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    """Delete thread"""
    thread_service = current_app.thread_service
    
    success = thread_service.delete_thread(thread_id)
    if success:
        return jsonify({"success": True})
    return jsonify({"error": "Thread not found"}), 404

