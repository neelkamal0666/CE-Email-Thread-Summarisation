"""
API Routes Package
"""
from .thread_routes import thread_bp
from .summary_routes import summary_bp
from .analytics_routes import analytics_bp
from .health_routes import health_bp

__all__ = ['thread_bp', 'summary_bp', 'analytics_bp', 'health_bp']


def register_blueprints(app):
    """Register all blueprints with the app"""
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(thread_bp, url_prefix='/api/threads')
    app.register_blueprint(summary_bp, url_prefix='/api/summaries')
    app.register_blueprint(analytics_bp, url_prefix='/api')

