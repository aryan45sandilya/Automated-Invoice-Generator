"""Settings routes for company configuration"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
import os
from dotenv import load_dotenv, set_key

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/')
@login_required
def index():
    """Settings page"""
    # Load current settings
    settings = {
        'company_name': current_app.config.get('COMPANY_NAME', 'Your Company'),
        'company_email': current_app.config.get('COMPANY_EMAIL', 'company@example.com'),
        'company_phone': current_app.config.get('COMPANY_PHONE', '+91-XXXXX-XXXXX'),
        'company_address': current_app.config.get('COMPANY_ADDRESS', 'Your Address'),
        'currency_symbol': current_app.config.get('CURRENCY_SYMBOL', '₹'),
        'currency_code': current_app.config.get('CURRENCY_CODE', 'INR'),
        'default_tax_rate': current_app.config.get('DEFAULT_TAX_RATE', 18.0),
        'invoice_prefix': current_app.config.get('INVOICE_PREFIX', 'INV'),
    }
    
    return render_template('settings/index.html', settings=settings)


@settings_bp.route('/update', methods=['POST'])
@login_required
def update():
    """Update company settings"""
    try:
        # Get form data
        company_name = request.form.get('company_name')
        company_email = request.form.get('company_email')
        company_phone = request.form.get('company_phone')
        company_address = request.form.get('company_address')
        currency_symbol = request.form.get('currency_symbol')
        currency_code = request.form.get('currency_code')
        default_tax_rate = request.form.get('default_tax_rate')
        invoice_prefix = request.form.get('invoice_prefix')
        
        # Path to .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        
        # Update .env file
        set_key(env_path, 'COMPANY_NAME', company_name)
        set_key(env_path, 'COMPANY_EMAIL', company_email)
        set_key(env_path, 'COMPANY_PHONE', company_phone)
        set_key(env_path, 'COMPANY_ADDRESS', company_address)
        set_key(env_path, 'CURRENCY_SYMBOL', currency_symbol)
        set_key(env_path, 'CURRENCY_CODE', currency_code)
        set_key(env_path, 'DEFAULT_TAX_RATE', default_tax_rate)
        set_key(env_path, 'INVOICE_PREFIX', invoice_prefix)
        
        # Update current app config
        current_app.config['COMPANY_NAME'] = company_name
        current_app.config['COMPANY_EMAIL'] = company_email
        current_app.config['COMPANY_PHONE'] = company_phone
        current_app.config['COMPANY_ADDRESS'] = company_address
        current_app.config['CURRENCY_SYMBOL'] = currency_symbol
        current_app.config['CURRENCY_CODE'] = currency_code
        current_app.config['DEFAULT_TAX_RATE'] = float(default_tax_rate)
        current_app.config['INVOICE_PREFIX'] = invoice_prefix
        
        flash('Settings updated successfully! Please restart the application for all changes to take effect.', 'success')
        return redirect(url_for('settings.index'))
        
    except Exception as e:
        flash(f'Error updating settings: {str(e)}', 'danger')
        return redirect(url_for('settings.index'))
