from flask import Flask, g
from flask_cors import CORS
from config import get_config
from models.database import Database
from services.thread_service import ThreadService
from services.summary_service import SummaryService
from services.nlp_service import NLPService
from services.analytics_service import AnalyticsService
from routes import register_blueprints


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})
    
    # Initialize database and services
    init_services(app, config)
    
    # Register blueprints
    register_blueprints(app)
    
    # Error handlers
    register_error_handlers(app)
    
    # Logging
    setup_logging(app, config)
    
    return app


def init_services(app, config):
    """Initialize all service instances and store in app context"""
    # Initialize database
    db = Database(config.DATABASE_PATH)
    print(f"Database initialized: {config.DATABASE_PATH}")
    
    # Initialize services
    app.thread_service = ThreadService(db)
    app.summary_service = SummaryService(db)
    app.nlp_service = NLPService(
        openai_api_key=config.OPENAI_API_KEY,
        model=config.OPENAI_MODEL,
        temperature=config.OPENAI_TEMPERATURE,
        max_tokens=config.OPENAI_MAX_TOKENS
    )
    app.analytics_service = AnalyticsService(db)
    
    # Log NLP method
    nlp_method = "OpenAI " + config.OPENAI_MODEL if config.OPENAI_API_KEY else "Rule-based"
    print(f"NLP Method: {nlp_method}")


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request"}, 400


def setup_logging(app, config):
    """Setup application logging"""
    if not config.DEBUG:
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Create logs directory if it doesn't exist
        import os
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configure file handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('CE Email Summarization startup')


def main():
    """Main entry point"""
    import os
    
    # Get configuration from environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Get config
    config = get_config(env)
    
    # Run app
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
