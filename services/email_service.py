from flask_mail import Mail, Message
from flask import current_app
import os


class EmailService:
    """Service for sending emails"""
    
    def __init__(self, mail):
        self.mail = mail
    
    def send_invoice_email(self, recipient_email, recipient_name, invoice, pdf_path):
        """
        Send invoice email with PDF attachment
        
        Args:
            recipient_email: Client email address
            recipient_name: Client name
            invoice: Invoice model instance
            pdf_path: Path to PDF file
        """
        try:
            subject = f"Invoice {invoice.invoice_number} from {current_app.config['COMPANY_NAME']}"
            
            body = f"""
Dear {recipient_name},

Thank you for your business! Please find attached invoice {invoice.invoice_number}.

Invoice Details:
- Invoice Number: {invoice.invoice_number}
- Date: {invoice.date.strftime('%B %d, %Y')}
- Due Date: {invoice.due_date.strftime('%B %d, %Y')}
- Amount: {current_app.config['CURRENCY_SYMBOL']}{invoice.total_amount:.2f}
- Status: {invoice.status}

Please make the payment by the due date to avoid any late fees.

If you have any questions about this invoice, please contact us.

Best regards,
{current_app.config['COMPANY_NAME']}
{current_app.config['COMPANY_EMAIL']}
{current_app.config['COMPANY_PHONE']}
            """
            
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body
            )
            
            # Attach PDF
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as pdf_file:
                    msg.attach(
                        f"Invoice_{invoice.invoice_number}.pdf",
                        "application/pdf",
                        pdf_file.read()
                    )
            
            self.mail.send(msg)
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_payment_reminder(self, recipient_email, recipient_name, invoice):
        """
        Send payment reminder email
        
        Args:
            recipient_email: Client email address
            recipient_name: Client name
            invoice: Invoice model instance
        """
        try:
            subject = f"Payment Reminder - Invoice {invoice.invoice_number}"
            
            body = f"""
Dear {recipient_name},

This is a friendly reminder that invoice {invoice.invoice_number} is due for payment.

Invoice Details:
- Invoice Number: {invoice.invoice_number}
- Due Date: {invoice.due_date.strftime('%B %d, %Y')}
- Amount Due: {current_app.config['CURRENCY_SYMBOL']}{invoice.total_amount:.2f}
- Status: {invoice.status}

Please arrange payment at your earliest convenience.

If you have already made the payment, please disregard this reminder.

Best regards,
{current_app.config['COMPANY_NAME']}
{current_app.config['COMPANY_EMAIL']}
{current_app.config['COMPANY_PHONE']}
            """
            
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body
            )
            
            self.mail.send(msg)
            return True, "Reminder sent successfully"
            
        except Exception as e:
            return False, f"Failed to send reminder: {str(e)}"
    
    def send_payment_confirmation(self, recipient_email, recipient_name, invoice):
        """
        Send payment confirmation email
        
        Args:
            recipient_email: Client email address
            recipient_name: Client name
            invoice: Invoice model instance
        """
        try:
            subject = f"Payment Received - Invoice {invoice.invoice_number}"
            
            body = f"""
Dear {recipient_name},

Thank you! We have received your payment for invoice {invoice.invoice_number}.

Payment Details:
- Invoice Number: {invoice.invoice_number}
- Amount Paid: {current_app.config['CURRENCY_SYMBOL']}{invoice.total_amount:.2f}
- Payment Date: {invoice.paid_at.strftime('%B %d, %Y') if invoice.paid_at else 'N/A'}

We appreciate your business and look forward to serving you again.

Best regards,
{current_app.config['COMPANY_NAME']}
{current_app.config['COMPANY_EMAIL']}
{current_app.config['COMPANY_PHONE']}
            """
            
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body
            )
            
            self.mail.send(msg)
            return True, "Confirmation sent successfully"
            
        except Exception as e:
            return False, f"Failed to send confirmation: {str(e)}"
