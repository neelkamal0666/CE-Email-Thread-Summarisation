"""
Health Check Routes
"""
from flask import Blueprint, jsonify, current_app
from datetime import datetime

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    nlp_service = current_app.nlp_service
    
    nlp_method = "openai" if nlp_service.openai_api_key else "rule_based"
    
    return jsonify({
        "status": "healthy",
        "nlp_method": nlp_method,
        "timestamp": datetime.now().isoformat()
    })

