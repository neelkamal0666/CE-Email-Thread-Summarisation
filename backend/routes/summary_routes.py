"""
Summary API Routes
"""
from flask import Blueprint, request, jsonify, current_app

summary_bp = Blueprint('summaries', __name__)


@summary_bp.route('', methods=['GET'])
def get_summaries():
    """Get all summaries"""
    summary_service = current_app.summary_service
    
    status = request.args.get('status')
    summaries = summary_service.get_all_summaries(status)
    
    return jsonify([summary.to_dict() for summary in summaries])


@summary_bp.route('/<int:summary_id>', methods=['GET'])
def get_summary(summary_id):
    """Get specific summary"""
    summary_service = current_app.summary_service
    
    summary = summary_service.get_summary_by_id(summary_id)
    if not summary:
        return jsonify({"error": "Summary not found"}), 404
    
    return jsonify(summary.to_dict())


@summary_bp.route('/<int:summary_id>/edit', methods=['PUT'])
def edit_summary(summary_id):
    """Edit a summary"""
    summary_service = current_app.summary_service
    
    try:
        data = request.json
        edited_summary = data.get('edited_summary')
        user = data.get('user', 'anonymous')
        
        if not edited_summary:
            return jsonify({"error": "edited_summary is required"}), 400
        
        success = summary_service.update_summary(summary_id, edited_summary, user)
        
        if success:
            return jsonify({"success": True})
        return jsonify({"error": "Summary not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@summary_bp.route('/<int:summary_id>/approve', methods=['POST'])
def approve_summary(summary_id):
    """Approve a summary"""
    summary_service = current_app.summary_service
    
    try:
        data = request.json
        user = data.get('user', 'anonymous')
        
        success = summary_service.approve_summary(summary_id, user)
        
        if success:
            return jsonify({"success": True})
        return jsonify({"error": "Summary not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@summary_bp.route('/<int:summary_id>/reject', methods=['POST'])
def reject_summary(summary_id):
    """Reject a summary"""
    summary_service = current_app.summary_service
    
    try:
        data = request.json
        user = data.get('user', 'anonymous')
        reason = data.get('reason', '')
        
        success = summary_service.reject_summary(summary_id, user, reason)
        
        if success:
            return jsonify({"success": True})
        return jsonify({"error": "Summary not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

