from datetime import datetime
from . import db


class Client(db.Model):
    """Client model for storing customer information"""
    
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    company = db.Column(db.String(100))
    gstin = db.Column(db.String(15))  # GST Identification Number (India)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoices = db.relationship('Invoice', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert client object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'company': self.company,
            'gstin': self.gstin,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_invoices': self.invoices.count()
        }
    
    def get_total_revenue(self):
        """Calculate total revenue from this client"""
        total = db.session.query(db.func.sum(db.text('invoices.total_amount')))\
            .filter(db.text('invoices.client_id = :client_id'))\
            .params(client_id=self.id)\
            .scalar()
        return float(total) if total else 0.0
    
    def get_pending_amount(self):
        """Calculate pending payment amount from this client"""
        from .invoice import Invoice
        total = db.session.query(db.func.sum(Invoice.total_amount))\
            .filter(Invoice.client_id == self.id, Invoice.status == 'Pending')\
            .scalar()
        return float(total) if total else 0.0
    
    def __repr__(self):
        return f'<Client {self.name}>'
