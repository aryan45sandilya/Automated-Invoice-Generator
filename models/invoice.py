from datetime import datetime, date
from . import db


class Invoice(db.Model):
    """Invoice model for storing invoice information"""
    
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, index=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Dates
    date = db.Column(db.Date, default=date.today, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    
    # Financial details
    subtotal = db.Column(db.Float, default=0.0, nullable=False)
    tax_rate = db.Column(db.Float, default=0.0, nullable=False)  # Percentage
    tax_amount = db.Column(db.Float, default=0.0, nullable=False)
    discount = db.Column(db.Float, default=0.0, nullable=False)
    total_amount = db.Column(db.Float, default=0.0, nullable=False)
    
    # Status: Pending, Paid, Overdue, Cancelled
    status = db.Column(db.String(20), default='Pending', nullable=False, index=True)
    
    # Additional info
    notes = db.Column(db.Text)
    terms = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('InvoiceItem', backref='invoice', lazy='dynamic', cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calculate invoice totals based on items"""
        # Calculate subtotal from items
        self.subtotal = sum(item.total for item in self.items)
        
        # Calculate tax
        self.tax_amount = (self.subtotal * self.tax_rate) / 100
        
        # Calculate total
        self.total_amount = self.subtotal + self.tax_amount - self.discount
    
    def update_status(self):
        """Update invoice status based on due date"""
        if self.status == 'Pending' and self.due_date < date.today():
            self.status = 'Overdue'
    
    def mark_as_paid(self):
        """Mark invoice as paid"""
        self.status = 'Paid'
        self.paid_at = datetime.utcnow()
    
    def to_dict(self, include_items=False):
        """Convert invoice object to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'client_id': self.client_id,
            'client_name': self.client.name if self.client else None,
            'invoice_number': self.invoice_number,
            'date': self.date.isoformat() if self.date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'subtotal': self.subtotal,
            'tax_rate': self.tax_rate,
            'tax_amount': self.tax_amount,
            'discount': self.discount,
            'total_amount': self.total_amount,
            'status': self.status,
            'notes': self.notes,
            'terms': self.terms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        
        return data
    
    @staticmethod
    def generate_invoice_number(user_id, prefix='INV'):
        """Generate unique invoice number"""
        from datetime import datetime
        
        # Format: INV-2026-000001
        year = datetime.now().year
        
        # Get the count of invoices for this user and year
        count = Invoice.query.filter(
            Invoice.user_id == user_id,
            Invoice.invoice_number.like(f'{prefix}-{year}-%')
        ).count()
        
        # Try to generate a unique number
        max_attempts = 100
        for attempt in range(max_attempts):
            new_number = count + attempt + 1
            invoice_number = f'{prefix}-{year}-{new_number:06d}'
            
            # Check if this number already exists
            existing = Invoice.query.filter_by(invoice_number=invoice_number).first()
            if not existing:
                return invoice_number
        
        # Fallback: use timestamp
        import time
        timestamp = int(time.time() * 1000) % 1000000
        return f'{prefix}-{year}-{timestamp:06d}'
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'
