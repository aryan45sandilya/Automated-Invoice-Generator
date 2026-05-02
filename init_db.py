"""
Database initialization script
Run this to create the database tables
"""

from app import create_app
from models import db, User, Client, Invoice, InvoiceItem
import os


def init_database():
    """Initialize the database with tables"""
    
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Optional: Create a demo user
        create_demo = input("\nDo you want to create a demo user? (y/n): ").lower()
        
        if create_demo == 'y':
            demo_user = User.query.filter_by(email='demo@example.com').first()
            
            if not demo_user:
                demo_user = User(
                    name='Demo User',
                    email='demo@example.com'
                )
                demo_user.set_password('demo123')
                db.session.add(demo_user)
                db.session.commit()
                
                print("\n✓ Demo user created!")
                print("  Email: demo@example.com")
                print("  Password: demo123")
                
                # Create demo client
                demo_client = Client(
                    user_id=demo_user.id,
                    name='Acme Corporation',
                    email='contact@acme.com',
                    phone='+1-555-0123',
                    address='123 Business Ave, Suite 100, New York, NY 10001',
                    company='Acme Corp',
                    notes='Demo client for testing'
                )
                db.session.add(demo_client)
                db.session.commit()
                
                print("✓ Demo client created!")
                
            else:
                print("\n⚠ Demo user already exists!")


if __name__ == '__main__':
    init_database()
