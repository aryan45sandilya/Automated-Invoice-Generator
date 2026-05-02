from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from models import db, Invoice, InvoiceItem, Client
from services import PDFGenerator, EmailService
from datetime import datetime, timedelta
import os

invoices_bp = Blueprint('invoices', __name__)


@invoices_bp.route('/')
@login_required
def list():
    """List all invoices"""
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.created_at.desc()).all()
    
    # Update status for all invoices
    for invoice in invoices:
        if invoice.status == 'Pending' and invoice.due_date < datetime.now().date():
            invoice.status = 'Overdue'
    db.session.commit()
    
    return render_template('invoices/list.html', invoices=invoices)


@invoices_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new invoice"""
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name).all()
    
    if request.method == 'POST':
        try:
            # Get form data
            client_id = request.form.get('client_id', type=int)
            date_str = request.form.get('date')
            due_date_str = request.form.get('due_date')
            tax_rate = request.form.get('tax_rate', 0, type=float)
            discount = request.form.get('discount', 0, type=float)
            notes = request.form.get('notes', '')
            status = request.form.get('status', 'Pending')
            
            # Validation
            if not client_id:
                flash('Please select a client.', 'danger')
                return render_template('invoices/form.html', clients=clients)
            
            client = Client.query.filter_by(id=client_id, user_id=current_user.id).first()
            if not client:
                flash('Invalid client selected.', 'danger')
                return render_template('invoices/form.html', clients=clients)
            
            # Parse dates
            invoice_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else (datetime.now() + timedelta(days=30)).date()
            
            # Create invoice
            invoice = Invoice(
                user_id=current_user.id,
                client_id=client_id,
                invoice_number=Invoice.generate_invoice_number(current_user.id),
                date=invoice_date,
                due_date=due_date,
                tax_rate=tax_rate,
                discount=discount,
                notes=notes,
                status=status,
                subtotal=0,
                tax_amount=0,
                total_amount=0
            )
            
            db.session.add(invoice)
            db.session.flush()  # Get invoice ID
            
            # Add items - handle both array formats
            items_data = []
            i = 0
            while True:
                desc = request.form.get(f'items[{i}][description]')
                if not desc:
                    break
                qty = request.form.get(f'items[{i}][quantity]', type=float)
                price = request.form.get(f'items[{i}][price]', type=float)
                if desc and qty and price:
                    items_data.append((desc, qty, price))
                i += 1
            
            if not items_data:
                flash('Please add at least one item.', 'danger')
                db.session.rollback()
                return render_template('invoices/form.html', clients=clients)
            
            for desc, qty, price in items_data:
                total = qty * price
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    description=desc,
                    quantity=qty,
                    price=price,
                    total=total
                )
                db.session.add(item)
            
            # Calculate totals
            subtotal = sum(item[1] * item[2] for item in items_data)
            tax_amount = (subtotal * tax_rate) / 100
            total_amount = subtotal + tax_amount - discount
            
            invoice.subtotal = subtotal
            invoice.tax_amount = tax_amount
            invoice.total_amount = total_amount
            
            db.session.commit()
            
            flash(f'Invoice {invoice.invoice_number} created successfully!', 'success')
            return redirect(url_for('invoices.view', invoice_id=invoice.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating invoice: {str(e)}', 'danger')
            return render_template('invoices/form.html', clients=clients)
    
    return render_template('invoices/form.html', clients=clients)


@invoices_bp.route('/<int:invoice_id>')
@login_required
def view(invoice_id):
    """View invoice details"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    
    # Update status if overdue
    if invoice.status == 'Pending' and invoice.due_date < datetime.now().date():
        invoice.status = 'Overdue'
        db.session.commit()
    
    return render_template('invoices/view.html', invoice=invoice)


@invoices_bp.route('/<int:invoice_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(invoice_id):
    """Edit invoice"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name).all()
    
    # Don't allow editing paid invoices
    if invoice.status == 'Paid':
        flash('Cannot edit paid invoices.', 'warning')
        return redirect(url_for('invoices.view', invoice_id=invoice.id))
    
    if request.method == 'POST':
        try:
            # Update invoice details
            date_str = request.form.get('date')
            due_date_str = request.form.get('due_date')
            invoice.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else invoice.date
            invoice.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else invoice.due_date
            invoice.tax_rate = request.form.get('tax_rate', 0, type=float)
            invoice.discount = request.form.get('discount', 0, type=float)
            invoice.notes = request.form.get('notes', '')
            invoice.status = request.form.get('status', 'Pending')
            
            # Delete existing items
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
            
            # Add updated items
            items_data = []
            i = 0
            while True:
                desc = request.form.get(f'items[{i}][description]')
                if not desc:
                    break
                qty = request.form.get(f'items[{i}][quantity]', type=float)
                price = request.form.get(f'items[{i}][price]', type=float)
                if desc and qty and price:
                    items_data.append((desc, qty, price))
                i += 1
            
            for desc, qty, price in items_data:
                total = qty * price
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    description=desc,
                    quantity=qty,
                    price=price,
                    total=total
                )
                db.session.add(item)
            
            # Recalculate totals
            subtotal = sum(item[1] * item[2] for item in items_data)
            tax_amount = (subtotal * invoice.tax_rate) / 100
            total_amount = subtotal + tax_amount - invoice.discount
            
            invoice.subtotal = subtotal
            invoice.tax_amount = tax_amount
            invoice.total_amount = total_amount
            
            db.session.commit()
            
            flash(f'Invoice {invoice.invoice_number} updated successfully!', 'success')
            return redirect(url_for('invoices.view', invoice_id=invoice.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating invoice: {str(e)}', 'danger')
    
    return render_template('invoices/form.html', invoice=invoice, clients=clients)


@invoices_bp.route('/<int:invoice_id>', methods=['DELETE'])
@login_required
def delete(invoice_id):
    """Delete invoice"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    
    # Don't allow deleting paid invoices
    if invoice.status == 'Paid':
        return jsonify({'success': False, 'message': 'Cannot delete paid invoices.'}), 400
    
    invoice_number = invoice.invoice_number
    db.session.delete(invoice)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Invoice {invoice_number} deleted successfully.'})


@invoices_bp.route('/<int:invoice_id>/status', methods=['PUT'])
@login_required
def update_status(invoice_id):
    """Update invoice status"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['Pending', 'Paid', 'Overdue', 'Cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status.'}), 400
    
    invoice.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Invoice status updated to {new_status}.'})


@invoices_bp.route('/<int:invoice_id>/pdf')
@login_required
def download_pdf(invoice_id):
    """Generate and download invoice PDF"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    client = invoice.client
    items = invoice.items.all()
    
    # Generate PDF
    pdf_dir = 'static/invoices'
    os.makedirs(pdf_dir, exist_ok=True)
    
    filename = os.path.join(pdf_dir, f'invoice_{invoice.invoice_number}.pdf')
    
    pdf_generator = PDFGenerator(current_app.config)
    pdf_generator.generate_invoice(invoice, client, items, filename)
    
    return send_file(filename, as_attachment=True, download_name=f'Invoice_{invoice.invoice_number}.pdf')


@invoices_bp.route('/<int:invoice_id>/email', methods=['POST'])
@login_required
def send_email(invoice_id):
    """Send invoice via email"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    client = invoice.client
    items = invoice.items.all()
    
    try:
        # Generate PDF
        pdf_dir = 'static/invoices'
        os.makedirs(pdf_dir, exist_ok=True)
        filename = os.path.join(pdf_dir, f'invoice_{invoice.invoice_number}.pdf')
        
        pdf_generator = PDFGenerator(current_app.config)
        pdf_generator.generate_invoice(invoice, client, items, filename)
        
        # Send email
        from flask_mail import Mail
        mail = Mail(current_app)
        email_service = EmailService(mail)
        
        success, message = email_service.send_invoice_email(
            client.email,
            client.name,
            invoice,
            filename
        )
        
        if success:
            return jsonify({'success': True, 'message': f'Invoice sent to {client.email} successfully!'})
        else:
            return jsonify({'success': False, 'message': f'Failed to send email: {message}'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error sending email: {str(e)}'}), 500


@invoices_bp.route('/<int:invoice_id>/reminder', methods=['POST'])
@login_required
def send_reminder(invoice_id):
    """Send payment reminder"""
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    client = invoice.client
    
    try:
        from flask_mail import Mail
        mail = Mail(current_app)
        email_service = EmailService(mail)
        
        success, message = email_service.send_payment_reminder(
            client.email,
            client.name,
            invoice
        )
        
        if success:
            flash(f'Payment reminder sent to {client.email}!', 'success')
        else:
            flash(f'Failed to send reminder: {message}', 'danger')
            
    except Exception as e:
        flash(f'Error sending reminder: {str(e)}', 'danger')
    
    return redirect(url_for('invoices.view', invoice_id=invoice.id))
