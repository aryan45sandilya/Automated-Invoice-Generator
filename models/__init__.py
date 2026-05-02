from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models for easy access
from .user import User
from .client import Client
from .invoice import Invoice
from .invoice_item import InvoiceItem

__all__ = ['db', 'User', 'Client', 'Invoice', 'InvoiceItem']
