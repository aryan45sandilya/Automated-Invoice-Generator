import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_url = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "invoices.db")}')
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Application Settings
    INVOICES_PER_PAGE = int(os.getenv('INVOICES_PER_PAGE', 10))
    COMPANY_NAME = os.getenv('COMPANY_NAME', 'Your Company')
    COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'company@example.com')
    COMPANY_PHONE = os.getenv('COMPANY_PHONE', '+1-234-567-8900')
    COMPANY_ADDRESS = os.getenv('COMPANY_ADDRESS', '123 Business St, City, Country')
    
    # Tax Configuration
    DEFAULT_TAX_RATE = float(os.getenv('DEFAULT_TAX_RATE', 18.0))
    CURRENCY_SYMBOL = os.getenv('CURRENCY_SYMBOL', '₹')
    CURRENCY_CODE = os.getenv('CURRENCY_CODE', 'INR')
    
    # Invoice Settings
    INVOICE_PREFIX = os.getenv('INVOICE_PREFIX', 'INV')
    INVOICE_NUMBER_LENGTH = int(os.getenv('INVOICE_NUMBER_LENGTH', 6))
    
    # Upload folder
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
