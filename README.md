<div align="center">

# 🧾 InvoiceHub

### Professional Invoice Management System

*Create, manage, and track invoices with style and efficiency*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

[Features](#-features) • [Installation](#-quick-start) • [Tech Stack](#-tech-stack) • [Screenshots](#-screenshots) • [Documentation](#-documentation)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 Core Features
- ✅ **Professional Invoices** - Create beautiful, detailed invoices
- ✅ **PDF Generation** - Download invoices as PDF
- ✅ **Client Management** - Store and manage client details
- ✅ **Status Tracking** - Track Paid/Pending/Overdue invoices
- ✅ **Auto Numbering** - Automatic invoice numbering (INV-2026-001)
- ✅ **Dashboard Analytics** - Real-time revenue and invoice stats

</td>
<td width="50%">

### 🚀 Advanced Features
- 📧 **Email Integration** - Send invoices directly to clients
- 💰 **Tax Configuration** - GST/Tax rate customization
- 🏢 **Company Settings** - Customize company details
- 👥 **Multi-user Support** - Secure authentication system
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Modern UI** - Beautiful gradient theme with animations

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation Steps

**1. Clone or Download the Project**
```bash
cd invoice_management_system
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
# Windows (recommended)
pip install -r requirements-windows.txt

# Linux/Mac
pip install -r requirements.txt
```

**4. Setup Environment**
```bash
# Copy example environment file
copy .env.example .env

# Edit .env file with your settings (optional)
```

**5. Initialize Database**
```bash
python init_db.py
```

**6. Run the Application**
```bash
python app.py
```

**7. Access the Application**
```
Open your browser and visit: http://localhost:5000

Demo Login:
Email: demo@example.com
Password: demo123
```

### 🎯 Quick Start Script

**Windows:**
```bash
quick_start.bat
```

**Linux/Mac:**
```bash
chmod +x quick_start.sh
./quick_start.sh
```

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/96/000000/python.png" width="48" height="48" alt="Python"/>
<br><strong>Python 3.9+</strong>
<br><sub>Backend Language</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/96/000000/flask.png" width="48" height="48" alt="Flask"/>
<br><strong>Flask</strong>
<br><sub>Web Framework</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/96/000000/bootstrap.png" width="48" height="48" alt="Bootstrap"/>
<br><strong>Bootstrap 5</strong>
<br><sub>UI Framework</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/96/000000/sqlite.png" width="48" height="48" alt="SQLite"/>
<br><strong>SQLite</strong>
<br><sub>Database</sub>
</td>
</tr>
</table>

### Backend
- **Flask** - Lightweight web framework
- **Flask-Login** - User session management
- **Flask-SQLAlchemy** - ORM for database
- **Werkzeug** - Password hashing (bcrypt)
- **python-dotenv** - Environment configuration

### PDF & Email
- **ReportLab** - PDF generation
- **Pillow** - Image processing
- **SMTP** - Email delivery

### Frontend
- **Bootstrap 5** - Responsive UI components
- **Bootstrap Icons** - Icon library
- **Google Fonts (Inter)** - Modern typography
- **Custom CSS** - Gradient theme with animations

---

## 📁 Project Structure

```
invoice_management_system/
│
├── 📄 app.py                    # Main application entry point
├── ⚙️ config.py                 # Configuration settings
├── 🗄️ init_db.py                # Database initialization
├── 📦 requirements.txt          # Python dependencies
├── 🪟 requirements-windows.txt  # Windows-specific dependencies
├── 🔐 .env                      # Environment variables
├── 📖 README.md                 # This file
│
├── 📂 models/                   # Database Models
│   ├── user.py                  # User model
│   ├── client.py                # Client model
│   ├── invoice.py               # Invoice model
│   └── invoice_item.py          # Invoice item model
│
├── 📂 routes/                   # Application Routes
│   ├── auth.py                  # Authentication routes
│   ├── clients.py               # Client management routes
│   ├── invoices.py              # Invoice management routes
│   ├── dashboard.py             # Dashboard routes
│   └── settings.py              # Settings routes
│
├── 📂 services/                 # Business Logic
│   ├── pdf_generator.py         # PDF generation service
│   ├── email_service.py         # Email sending service
│   └── invoice_calculator.py    # Invoice calculations
│
├── 📂 templates/                # HTML Templates
│   ├── base.html                # Base layout
│   ├── auth/                    # Login & Register
│   ├── dashboard/               # Dashboard views
│   ├── clients/                 # Client views
│   ├── invoices/                # Invoice views
│   ├── settings/                # Settings views
│   └── errors/                  # Error pages
│
├── 📂 static/                   # Static Files
│   ├── css/
│   │   └── style.css            # Custom styles
│   ├── js/
│   │   └── main.js              # Custom JavaScript
│   └── invoices/                # Generated PDF invoices
│
└── 📂 database/                 # Database Files
    └── invoices.db              # SQLite database
```

---

## 🗄️ Database Schema

### 👤 Users Table
```sql
- id (Primary Key)
- name (VARCHAR)
- email (VARCHAR, Unique)
- password_hash (VARCHAR)
- created_at (TIMESTAMP)
```

### 👥 Clients Table
```sql
- id (Primary Key)
- user_id (Foreign Key → Users)
- name (VARCHAR)
- email (VARCHAR)
- phone (VARCHAR)
- address (TEXT)
- created_at (TIMESTAMP)
```

### 📄 Invoices Table
```sql
- id (Primary Key)
- client_id (Foreign Key → Clients)
- user_id (Foreign Key → Users)
- invoice_number (VARCHAR, Unique)
- date (DATE)
- due_date (DATE)
- subtotal (DECIMAL)
- tax_rate (DECIMAL)
- tax_amount (DECIMAL)
- discount (DECIMAL)
- total_amount (DECIMAL)
- status (ENUM: Pending/Paid/Overdue/Draft)
- notes (TEXT)
- created_at (TIMESTAMP)
```

### 📋 Invoice Items Table
```sql
- id (Primary Key)
- invoice_id (Foreign Key → Invoices)
- description (VARCHAR)
- quantity (INTEGER)
- price (DECIMAL)
- total (DECIMAL)
```

---

## 🎨 Screenshots

### 🔐 Login Page
Beautiful gradient background with modern glassmorphism design

### 📊 Dashboard
Real-time analytics with colorful stats cards and revenue charts

### 👥 Client Management
Easy-to-use interface for managing client information

### 🧾 Invoice Creation
Intuitive form with dynamic item addition and automatic calculations

### 📄 PDF Invoice
Professional PDF invoices with company branding

### ⚙️ Settings
Customize company details, currency, and tax rates

---

## 🔌 API Routes

### 🔐 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/login` | Login page |
| `POST` | `/auth/login` | Process login |
| `GET` | `/auth/register` | Registration page |
| `POST` | `/auth/register` | Process registration |
| `GET` | `/auth/logout` | Logout user |

### 👥 Clients
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/clients` | List all clients |
| `GET` | `/clients/new` | New client form |
| `POST` | `/clients/new` | Create client |
| `GET` | `/clients/<id>` | View client details |
| `GET` | `/clients/<id>/edit` | Edit client form |
| `POST` | `/clients/<id>/edit` | Update client |
| `POST` | `/clients/<id>/delete` | Delete client |

### 🧾 Invoices
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/invoices` | List all invoices |
| `GET` | `/invoices/new` | New invoice form |
| `POST` | `/invoices/new` | Create invoice |
| `GET` | `/invoices/<id>` | View invoice details |
| `GET` | `/invoices/<id>/edit` | Edit invoice form |
| `POST` | `/invoices/<id>/edit` | Update invoice |
| `POST` | `/invoices/<id>/delete` | Delete invoice |
| `GET` | `/invoices/<id>/pdf` | Download PDF |
| `POST` | `/invoices/<id>/email` | Email invoice |
| `POST` | `/invoices/<id>/status` | Update status |

### 📊 Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard` | Dashboard analytics |

### ⚙️ Settings
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/settings` | Settings page |
| `POST` | `/settings` | Update settings |

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///invoices.db

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Company Settings
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=company@example.com
COMPANY_PHONE=+91-XXXXX-XXXXX
COMPANY_ADDRESS=Your Company Address

# Invoice Settings
CURRENCY_SYMBOL=₹
CURRENCY_CODE=INR
DEFAULT_TAX_RATE=18.0
INVOICE_PREFIX=INV
```

---

## 🎯 Usage Guide

### Creating Your First Invoice

1. **Login** to the system
2. **Add a Client** from the Clients page
3. **Create Invoice** from the Invoices page
4. **Add Items** with description, quantity, and price
5. **Review** the auto-calculated totals
6. **Save** the invoice
7. **Download PDF** or **Email** to client

### Managing Clients

- Add new clients with contact details
- View client history and invoices
- Edit or delete client information
- Track total invoices per client

### Dashboard Analytics

- View total revenue
- Track pending and overdue amounts
- See total client count
- Monitor monthly revenue trends
- View top clients

### Customizing Settings

- Update company information
- Change currency and tax rates
- Modify invoice prefix
- Configure email settings

---

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment

**Using Gunicorn (Linux/Mac):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Using Waitress (Windows):**
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Docker Deployment
```bash
# Build image
docker build -t invoicehub .

# Run container
docker run -p 5000:5000 invoicehub
```

### Cloud Platforms
- **Render**: Connect GitHub repo and deploy
- **Railway**: One-click deployment
- **Heroku**: Use Procfile for deployment
- **PythonAnywhere**: Upload and configure

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Pillow installation fails on Windows**
```bash
# Solution: Use pre-built wheel
pip install -r requirements-windows.txt
```

**Issue: Database not found**
```bash
# Solution: Initialize database
python init_db.py
```

**Issue: Port 5000 already in use**
```bash
# Solution: Change port in app.py
app.run(debug=True, port=5001)
```

**Issue: CSS not loading**
```bash
# Solution: Clear browser cache
Ctrl + Shift + Delete (or Cmd + Shift + Delete on Mac)
Ctrl + F5 for hard refresh
```

---

## 📚 Documentation

### Additional Resources

- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Detailed setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference guide
- [SETTINGS_GUIDE.md](SETTINGS_GUIDE.md) - Settings configuration

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 Report bugs
2. 💡 Suggest new features
3. 📝 Improve documentation
4. 🔧 Submit pull requests

---

## 📞 Support

Need help? Here are some resources:

- 📧 Email: support@invoicehub.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/invoicehub/issues)
- 📖 Documentation: Check the docs folder

---

## 🙏 Acknowledgments

- **Flask** - Amazing web framework
- **Bootstrap** - Beautiful UI components
- **ReportLab** - PDF generation library
- **Google Fonts** - Inter font family

---

<div align="center">

### Made with ❤️ for Freelancers and Small Businesses

**InvoiceHub** - *Simplifying Invoice Management*

⭐ Star this repo if you find it helpful!

</div>
