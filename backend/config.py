"""
Application Configuration
"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING: bool = False
    
    # Database
    DATABASE_PATH: str = os.environ.get('DATABASE_PATH', 'ce_threads.db')
    
    # OpenAI
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.environ.get('OPENAI_MODEL', 'gpt-4')
    OPENAI_TEMPERATURE: float = float(os.environ.get('OPENAI_TEMPERATURE', '0.3'))
    OPENAI_MAX_TOKENS: int = int(os.environ.get('OPENAI_MAX_TOKENS', '500'))
    
    # CORS
    CORS_ORIGINS: str = os.environ.get('CORS_ORIGINS', '*')
    
    # Server
    HOST: str = os.environ.get('HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('PORT', '5000'))


@dataclass
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG: bool = True


@dataclass
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False
    # In production, require these to be set
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    
    def __post_init__(self):
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production")


@dataclass
class TestingConfig(Config):
    """Testing configuration"""
    TESTING: bool = True
    DATABASE_PATH: str = ':memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])()

