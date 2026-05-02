from . import db


class InvoiceItem(db.Model):
    """Invoice item model for storing individual line items"""
    
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, default=1.0, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    def calculate_total(self):
        """Calculate total for this item"""
        self.total = self.quantity * self.price
    
    def to_dict(self):
        """Convert invoice item to dictionary"""
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.total
        }
    
    def __repr__(self):
        return f'<InvoiceItem {self.description}>'
