"""
Analytics API Routes
"""
from flask import Blueprint, jsonify, current_app

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get analytics dashboard data"""
    analytics_service = current_app.analytics_service
    
    return jsonify(analytics_service.get_dashboard_analytics())


@analytics_bp.route('/export/<int:summary_id>', methods=['GET'])
def export_summary(summary_id):
    """Export approved summary for CRM/downstream use"""
    summary_service = current_app.summary_service
    
    export_data = summary_service.get_export_data(summary_id)
    
    if not export_data:
        return jsonify({"error": "Summary not found or not approved"}), 400
    
    return jsonify(export_data)

