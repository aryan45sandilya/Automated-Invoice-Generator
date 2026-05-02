from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_mail import Mail
import os

from config import config
from models import db, User
from services import PDFGenerator, EmailService

# Initialize extensions
login_manager = LoginManager()
mail = Mail()


def create_app(config_name='development'):
    """Application factory pattern"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure required directories exist
    os.makedirs('database', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/invoices', exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.clients import clients_bp
    from routes.invoices import invoices_bp
    from routes.settings import settings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    # Home route
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def utility_processor():
        import time
        return {
            'company_name': app.config['COMPANY_NAME'],
            'currency_symbol': app.config['CURRENCY_SYMBOL'],
            'cache_buster': int(time.time())  # Force browser to reload
        }
    
    return app


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
