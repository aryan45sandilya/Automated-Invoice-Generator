# 🚀 Quick Reference Guide

## ⚡ Quick Start Commands

### Setup (First Time)
```bash
cd invoice_management_system
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
copy .env.example .env         # Windows
cp .env.example .env           # Mac/Linux
python init_db.py
python app.py
```

### Daily Use
```bash
cd invoice_management_system
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
python app.py
```

---

## 🌐 URLs

- **Application**: http://localhost:5000
- **Login**: http://localhost:5000/auth/login
- **Register**: http://localhost:5000/auth/register
- **Dashboard**: http://localhost:5000/dashboard/
- **Clients**: http://localhost:5000/clients/
- **Invoices**: http://localhost:5000/invoices/

---

## 📁 Important Files

### Configuration
- `.env` - Environment variables (create from .env.example)
- `config.py` - Application configuration
- `requirements.txt` - Python dependencies

### Database
- `init_db.py` - Initialize database
- `database/invoices.db` - SQLite database (auto-created)

### Main Application
- `app.py` - Run this to start the server

---

## 🔑 Default Settings

### Server
- **Host**: 0.0.0.0
- **Port**: 5000
- **Debug**: True (development)

### Database
- **Type**: SQLite
- **Location**: database/invoices.db

### Email (Configure in .env)
- **Server**: smtp.gmail.com
- **Port**: 587
- **TLS**: True

### Invoice
- **Tax Rate**: 18% (configurable)
- **Currency**: $ (configurable)
- **Number Format**: INV-2026-000001

---

## 🎯 Common Tasks

### Create New Invoice
1. Login to application
2. Click "Invoices" in sidebar
3. Click "Create New Invoice"
4. Select client
5. Add items
6. Set tax/discount
7. Click "Create Invoice"

### Send Invoice Email
1. Open invoice
2. Click "Send Email" button
3. Confirm recipient
4. Email sent with PDF attachment

### Generate PDF
1. Open invoice
2. Click "Download PDF"
3. PDF downloads automatically

### Add New Client
1. Click "Clients" in sidebar
2. Click "Add New Client"
3. Fill in details
4. Click "Create Client"

---

## 🔧 Configuration Options

### .env File
```env
# Required
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database/invoices.db

# Company Info
COMPANY_NAME=Your Company
COMPANY_EMAIL=info@company.com
COMPANY_PHONE=+1-234-567-8900
COMPANY_ADDRESS=Your Address

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your-app-password

# Invoice Settings
DEFAULT_TAX_RATE=18.0
CURRENCY_SYMBOL=$
```

---

## 🐛 Quick Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Database Issues
```bash
# Reinitialize database
python init_db.py
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Email Not Working
- Check MAIL_USERNAME and MAIL_PASSWORD in .env
- For Gmail, use App Password (not regular password)
- Enable 2FA and generate App Password

---

## 📊 File Structure

```
invoice_management_system/
├── app.py                 # Start here
├── config.py              # Configuration
├── init_db.py            # Database setup
├── requirements.txt       # Dependencies
├── .env                  # Your settings
│
├── models/               # Database models
├── routes/               # URL handlers
├── services/             # Business logic
├── templates/            # HTML pages
└── static/              # CSS/JS/Images
```

---

## 🎨 Customization Quick Tips

### Change Company Name
Edit `.env`:
```env
COMPANY_NAME=Your Company Name
```

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #4e73df;
    --secondary-color: #858796;
}
```

### Change Tax Rate
Edit `.env`:
```env
DEFAULT_TAX_RATE=18.0
```

### Change Currency
Edit `.env`:
```env
CURRENCY_SYMBOL=$
```

---

## 📱 User Roles & Permissions

### Current Implementation
- All users have full access to their own data
- Users can only see their own clients and invoices
- No admin/user distinction (single-user per account)

### To Add Multi-User Support
- Add role field to User model
- Implement role-based access control
- Add team/organization model

---

## 🔐 Security Checklist

### Development
- [x] Password hashing enabled
- [x] Session management active
- [x] SQL injection protected
- [x] XSS protection enabled

### Production (Before Deploy)
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use PostgreSQL
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Enable CSRF protection
- [ ] Regular backups

---

## 📈 Performance Tips

### For Better Performance
1. Use PostgreSQL instead of SQLite
2. Add database indexes
3. Enable caching
4. Optimize queries
5. Use CDN for static files
6. Enable gzip compression
7. Add pagination for large lists

---

## 🚀 Deployment Quick Guide

### Render
```bash
# Build Command
pip install -r requirements.txt

# Start Command
gunicorn app:create_app()
```

### Railway
- Connect GitHub repo
- Add PostgreSQL
- Set environment variables
- Deploy automatically

### Docker
```bash
docker-compose up -d
```

---

## 📞 Quick Help

### Documentation Files
- `README.md` - Project overview
- `SETUP_INSTRUCTIONS.md` - Detailed setup
- `IMPLEMENTATION_GUIDE.md` - Implementation details
- `ARCHITECTURE.md` - System design
- `COMPLETION_SUMMARY.md` - What's included

### Quick Start Scripts
- `quick_start.bat` - Windows
- `quick_start.sh` - Mac/Linux

---

## 🎯 Testing Checklist

### Quick Test
1. [ ] Register new user
2. [ ] Login
3. [ ] Create client
4. [ ] Create invoice
5. [ ] Download PDF
6. [ ] View dashboard
7. [ ] Logout

### Full Test
- [ ] All CRUD operations for clients
- [ ] All CRUD operations for invoices
- [ ] PDF generation
- [ ] Email sending (if configured)
- [ ] Status updates
- [ ] Search/filter functionality
- [ ] Error pages (404, 500)

---

## 💡 Pro Tips

1. **Backup Database**: Copy `database/invoices.db` regularly
2. **Test Email**: Use Mailtrap.io for testing emails
3. **Version Control**: Use Git for tracking changes
4. **Environment**: Keep .env file secure and never commit it
5. **Updates**: Keep dependencies updated with `pip list --outdated`

---

## 🔗 Useful Links

### Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Bootstrap: https://getbootstrap.com/
- ReportLab: https://www.reportlab.com/

### Deployment
- Render: https://render.com
- Railway: https://railway.app
- Heroku: https://heroku.com

### Email Testing
- Mailtrap: https://mailtrap.io
- Gmail App Passwords: https://myaccount.google.com/apppasswords

---

## 📝 Quick Commands Reference

```bash
# Virtual Environment
python -m venv venv                    # Create
venv\Scripts\activate                  # Activate (Windows)
source venv/bin/activate               # Activate (Mac/Linux)
deactivate                             # Deactivate

# Dependencies
pip install -r requirements.txt        # Install all
pip freeze > requirements.txt          # Update list
pip list --outdated                    # Check updates

# Database
python init_db.py                      # Initialize
python -c "from app import db; db.create_all()"  # Create tables

# Run Application
python app.py                          # Development
gunicorn app:create_app()             # Production

# Docker
docker-compose up -d                   # Start
docker-compose down                    # Stop
docker-compose logs -f                 # View logs
```

---

## ✅ Pre-Launch Checklist

### Before First Use
- [ ] Install Python 3.9+
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Copy .env.example to .env
- [ ] Edit .env with your settings
- [ ] Run init_db.py
- [ ] Start application
- [ ] Register first user

### Before Production Deploy
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up email service
- [ ] Enable HTTPS
- [ ] Test all features
- [ ] Backup database
- [ ] Monitor logs

---

**Keep this file handy for quick reference! 📌**
