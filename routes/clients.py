from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Client

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/')
@login_required
def list():
    """List all clients"""
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.created_at.desc()).all()
    
    # Calculate total revenue for each client
    for client in clients:
        invoices = client.invoices.all()
        client.total_revenue = sum(invoice.total_amount for invoice in invoices if invoice.status == 'Paid')
    
    return render_template('clients/list.html', clients=clients)


@clients_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new client"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        company = request.form.get('company')
        gstin = request.form.get('gstin')
        
        # Validation
        if not name or not email:
            flash('Name and email are required.', 'danger')
            return render_template('clients/form.html')
        
        # Create client
        client = Client(
            user_id=current_user.id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            company=company,
            gstin=gstin
        )
        
        db.session.add(client)
        db.session.commit()
        
        flash(f'Client "{name}" created successfully!', 'success')
        return redirect(url_for('clients.view', client_id=client.id))
    
    return render_template('clients/form.html')


@clients_bp.route('/<int:client_id>')
@login_required
def view(client_id):
    """View client details"""
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    
    # Get all invoices for this client
    invoices = client.invoices.all()
    
    # Calculate statistics
    total_revenue = sum(invoice.total_amount for invoice in invoices)
    pending_amount = sum(invoice.total_amount for invoice in invoices if invoice.status in ['Pending', 'Overdue'])
    paid_amount = sum(invoice.total_amount for invoice in invoices if invoice.status == 'Paid')
    
    return render_template('clients/view.html',
                         client=client,
                         total_revenue=total_revenue,
                         pending_amount=pending_amount,
                         paid_amount=paid_amount)


@clients_bp.route('/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(client_id):
    """Edit client"""
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        client.name = request.form.get('name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.address = request.form.get('address')
        client.company = request.form.get('company')
        client.gstin = request.form.get('gstin')
        
        if not client.name or not client.email:
            flash('Name and email are required.', 'danger')
            return render_template('clients/form.html', client=client)
        
        db.session.commit()
        flash(f'Client "{client.name}" updated successfully!', 'success')
        return redirect(url_for('clients.view', client_id=client.id))
    
    return render_template('clients/form.html', client=client)


@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@login_required
def delete(client_id):
    """Delete client"""
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    
    # Check if client has invoices
    invoice_count = client.invoices.count()
    if invoice_count > 0:
        return jsonify({'success': False, 'message': 'Cannot delete client with existing invoices.'}), 400
    
    name = client.name
    db.session.delete(client)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Client "{name}" deleted successfully.'})


@clients_bp.route('/api/list')
@login_required
def api_list():
    """API endpoint to get clients list (for dropdowns)"""
    clients = Client.query.filter_by(user_id=current_user.id)\
        .order_by(Client.name)\
        .all()
    
    return jsonify([{
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'company': client.company
    } for client in clients])
