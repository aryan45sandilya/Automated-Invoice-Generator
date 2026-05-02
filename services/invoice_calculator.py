class InvoiceCalculator:
    """Service for invoice calculations"""
    
    @staticmethod
    def calculate_item_total(quantity, price):
        """Calculate total for a single item"""
        return round(quantity * price, 2)
    
    @staticmethod
    def calculate_subtotal(items):
        """Calculate subtotal from list of items"""
        return round(sum(item.total for item in items), 2)
    
    @staticmethod
    def calculate_tax(subtotal, tax_rate):
        """Calculate tax amount"""
        return round((subtotal * tax_rate) / 100, 2)
    
    @staticmethod
    def calculate_total(subtotal, tax_amount, discount=0):
        """Calculate final total"""
        return round(subtotal + tax_amount - discount, 2)
    
    @staticmethod
    def calculate_invoice_totals(invoice):
        """
        Calculate all totals for an invoice
        
        Args:
            invoice: Invoice model instance with items
            
        Returns:
            dict: Dictionary with calculated values
        """
        # Calculate subtotal from items
        subtotal = InvoiceCalculator.calculate_subtotal(invoice.items)
        
        # Calculate tax
        tax_amount = InvoiceCalculator.calculate_tax(subtotal, invoice.tax_rate)
        
        # Calculate total
        total = InvoiceCalculator.calculate_total(subtotal, tax_amount, invoice.discount)
        
        return {
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total_amount': total
        }
    
    @staticmethod
    def apply_discount(total, discount_type, discount_value):
        """
        Apply discount to total
        
        Args:
            total: Original total amount
            discount_type: 'percentage' or 'fixed'
            discount_value: Discount value
            
        Returns:
            tuple: (discount_amount, new_total)
        """
        if discount_type == 'percentage':
            discount_amount = round((total * discount_value) / 100, 2)
        else:  # fixed
            discount_amount = discount_value
        
        new_total = round(total - discount_amount, 2)
        return discount_amount, new_total
    
    @staticmethod
    def calculate_gst(subtotal, gst_rate=18.0):
        """
        Calculate GST (Goods and Services Tax) - India specific
        
        Args:
            subtotal: Subtotal amount
            gst_rate: GST rate (default 18%)
            
        Returns:
            dict: Dictionary with CGST, SGST, and total GST
        """
        total_gst = round((subtotal * gst_rate) / 100, 2)
        cgst = round(total_gst / 2, 2)  # Central GST
        sgst = round(total_gst / 2, 2)  # State GST
        
        return {
            'cgst': cgst,
            'sgst': sgst,
            'total_gst': total_gst,
            'gst_rate': gst_rate
        }
