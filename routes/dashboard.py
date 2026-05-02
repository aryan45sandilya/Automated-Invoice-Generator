from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, Invoice, Client
from sqlalchemy import func, extract
from datetime import datetime, timedelta, date

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard home page with analytics"""
    
    # Get statistics
    total_invoices = Invoice.query.filter_by(user_id=current_user.id).count()
    total_clients = Client.query.filter_by(user_id=current_user.id).count()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Invoice.total_amount))\
        .filter(Invoice.user_id == current_user.id, Invoice.status == 'Paid')\
        .scalar() or 0
    
    pending_amount = db.session.query(func.sum(Invoice.total_amount))\
        .filter(Invoice.user_id == current_user.id, Invoice.status == 'Pending')\
        .scalar() or 0
    
    overdue_amount = db.session.query(func.sum(Invoice.total_amount))\
        .filter(Invoice.user_id == current_user.id, Invoice.status == 'Overdue')\
        .scalar() or 0
    
    # Status counts
    paid_count = Invoice.query.filter_by(user_id=current_user.id, status='Paid').count()
    pending_count = Invoice.query.filter_by(user_id=current_user.id, status='Pending').count()
    overdue_count = Invoice.query.filter_by(user_id=current_user.id, status='Overdue').count()
    
    # Recent invoices
    recent_invoices = Invoice.query.filter_by(user_id=current_user.id)\
        .order_by(Invoice.created_at.desc())\
        .limit(5)\
        .all()
    
    # Monthly revenue (last 6 months)
    monthly_data = get_monthly_revenue(current_user.id)
    
    # Top clients by revenue
    top_clients = get_top_clients(current_user.id, limit=5)
    
    return render_template('dashboard/index.html',
                         total_invoices=total_invoices,
                         total_clients=total_clients,
                         total_revenue=total_revenue,
                         pending_amount=pending_amount,
                         overdue_amount=overdue_amount,
                         paid_count=paid_count,
                         pending_count=pending_count,
                         overdue_count=overdue_count,
                         recent_invoices=recent_invoices,
                         monthly_data=monthly_data,
                         top_clients=top_clients)


@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for dashboard statistics"""
    
    stats = {
        'total_invoices': Invoice.query.filter_by(user_id=current_user.id).count(),
        'total_clients': Client.query.filter_by(user_id=current_user.id).count(),
        'total_revenue': float(db.session.query(func.sum(Invoice.total_amount))
            .filter(Invoice.user_id == current_user.id, Invoice.status == 'Paid')
            .scalar() or 0),
        'pending_amount': float(db.session.query(func.sum(Invoice.total_amount))
            .filter(Invoice.user_id == current_user.id, Invoice.status == 'Pending')
            .scalar() or 0),
    }
    
    return jsonify(stats)


@dashboard_bp.route('/api/monthly-revenue')
@login_required
def api_monthly_revenue():
    """API endpoint for monthly revenue data"""
    months = int(request.args.get('months', 6))
    data = get_monthly_revenue(current_user.id, months)
    return jsonify(data)


def get_monthly_revenue(user_id, months=6):
    """Get monthly revenue for the last N months"""
    
    monthly_data = []
    current_date = datetime.now()
    
    for i in range(months - 1, -1, -1):
        # Calculate the target month
        target_date = current_date - timedelta(days=30 * i)
        month = target_date.month
        year = target_date.year
        
        # Query revenue for this month
        revenue = db.session.query(func.sum(Invoice.total_amount))\
            .filter(
                Invoice.user_id == user_id,
                Invoice.status == 'Paid',
                extract('month', Invoice.date) == month,
                extract('year', Invoice.date) == year
            ).scalar() or 0
        
        monthly_data.append({
            'month': target_date.strftime('%b %Y'),
            'revenue': float(revenue)
        })
    
    return monthly_data


def get_top_clients(user_id, limit=5):
    """Get top clients by total revenue"""
    
    top_clients = db.session.query(
        Client.id,
        Client.name,
        func.sum(Invoice.total_amount).label('total_revenue'),
        func.count(Invoice.id).label('invoice_count')
    ).join(Invoice, Invoice.client_id == Client.id)\
     .filter(Client.user_id == user_id, Invoice.status == 'Paid')\
     .group_by(Client.id, Client.name)\
     .order_by(func.sum(Invoice.total_amount).desc())\
     .limit(limit)\
     .all()
    
    return [{
        'id': client.id,
        'name': client.name,
        'total_revenue': float(client.total_revenue),
        'invoice_count': client.invoice_count
    } for client in top_clients]
