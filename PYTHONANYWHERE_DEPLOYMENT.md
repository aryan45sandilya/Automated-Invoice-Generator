# 🚀 PythonAnywhere Deployment Guide

## ✅ Why PythonAnywhere?
- ✅ **Completely FREE** forever
- ✅ **No credit card** needed
- ✅ **MySQL database** included
- ✅ **Easy setup** - beginner friendly
- ✅ **No sleep time** - always active
- ✅ **SSH access** available

---

## 📋 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in details:
   - Username (this will be your URL: `username.pythonanywhere.com`)
   - Email
   - Password
5. Verify email and login

---

### Step 2: Open Bash Console

1. After login, click **"Consoles"** tab
2. Click **"Bash"** (under "Start a new console")
3. A terminal will open

---

### Step 3: Clone Your GitHub Repository

In the Bash console, run:

```bash
# Clone your repository
git clone https://github.com/aryan45sandilya/Automated-Invoice-Generator.git

# Go to project folder
cd Automated-Invoice-Generator

# List files to verify
ls -la
```

---

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note:** This will take 5-10 minutes. Wait patiently!

---

### Step 5: Setup MySQL Database

1. Go to **"Databases"** tab in PythonAnywhere dashboard
2. Under **"Create a new database"**:
   - Database name: `invoicehub` (or any name)
   - Click **"Create"**
3. Note down:
   - **Host**: `username.mysql.pythonanywhere-services.com`
   - **Database name**: `username$invoicehub`
   - **Username**: `username` (your PythonAnywhere username)
4. Set a **password** for MySQL (if not set)

---

### Step 6: Update Configuration

In Bash console:

```bash
# Create .env file
nano .env
```

Add these lines (replace with your details):

```bash
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False

# Database (MySQL)
DATABASE_URL=mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$invoicehub

# Company Settings
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=your-email@example.com
COMPANY_PHONE=+91-XXXXX-XXXXX
COMPANY_ADDRESS=Your Company Address
CURRENCY_SYMBOL=₹
CURRENCY_CODE=INR
DEFAULT_TAX_RATE=18.0
INVOICE_PREFIX=INV
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

### Step 7: Install MySQL Connector

```bash
# Install PyMySQL for MySQL connection
pip install pymysql
```

---

### Step 8: Initialize Database

```bash
# Run database initialization
python init_db.py
```

You should see: "Database tables created successfully!"

---

### Step 9: Create Web App

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Click **"Next"** (for free domain)
4. Select **"Manual configuration"**
5. Choose **"Python 3.10"**
6. Click **"Next"**

---

### Step 10: Configure Web App

#### A. Set Source Code Path:
- **Source code**: `/home/username/Automated-Invoice-Generator`

#### B. Set Working Directory:
- **Working directory**: `/home/username/Automated-Invoice-Generator`

#### C. Set Virtual Environment:
- **Virtualenv**: `/home/username/Automated-Invoice-Generator/venv`

#### D. Edit WSGI Configuration File:

1. Click on **WSGI configuration file** link (e.g., `/var/www/username_pythonanywhere_com_wsgi.py`)
2. **Delete all content** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/username/Automated-Invoice-Generator'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application
```

**Replace `username` with your actual PythonAnywhere username!**

3. Click **"Save"** (top right)

---

### Step 11: Configure Static Files

In the **Web** tab, scroll to **"Static files"** section:

Add these mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/username/Automated-Invoice-Generator/static/` |

Click **"Save"**

---

### Step 12: Reload Web App

1. Scroll to top of **Web** tab
2. Click big green **"Reload username.pythonanywhere.com"** button
3. Wait 10-20 seconds

---

### Step 13: Access Your App! 🎉

Your app is now live at:
```
https://username.pythonanywhere.com
```

**Demo Login:**
- Email: `demo@example.com`
- Password: `demo123`

---

## 🔧 Troubleshooting

### Issue: 502 Bad Gateway

**Check Error Log:**
1. Web tab → **"Log files"**
2. Click **"Error log"**
3. See what error is showing

**Common fixes:**
```bash
# In Bash console
cd Automated-Invoice-Generator
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check if app runs
python app.py
```

### Issue: Database Connection Error

**Fix .env file:**
```bash
nano .env
# Verify DATABASE_URL is correct
# Format: mysql+pymysql://username:password@host/database
```

### Issue: Import Error

**Install missing package:**
```bash
source venv/bin/activate
pip install package-name
```

Then reload web app.

### Issue: Static Files Not Loading

**Check paths:**
- Static files mapping should be exact
- Path: `/home/username/Automated-Invoice-Generator/static/`

---

## 🔄 Updating Your App

When you make changes and push to GitHub:

```bash
# In PythonAnywhere Bash console
cd Automated-Invoice-Generator

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Reload web app (or click Reload button in Web tab)
touch /var/www/username_pythonanywhere_com_wsgi.py
```

---

## ⚙️ Important Notes

### Free Tier Limitations:
- ✅ One web app
- ✅ 512 MB disk space
- ✅ MySQL database (200 MB)
- ✅ Always-on (no sleep)
- ⚠️ Subdomain only (username.pythonanywhere.com)
- ⚠️ CPU seconds limited (100 seconds/day)

### Custom Domain (Paid):
- Need paid plan ($5/month) for custom domain

### Scheduled Tasks:
- Free tier: 1 scheduled task/day
- Can run cron jobs for backups, etc.

---

## 📝 Quick Commands Reference

### Access Bash Console:
```bash
cd Automated-Invoice-Generator
source venv/bin/activate
```

### View Logs:
```bash
# Error log
tail -f /var/log/username.pythonanywhere.com.error.log

# Access log
tail -f /var/log/username.pythonanywhere.com.access.log
```

### Restart App:
```bash
# Touch WSGI file to reload
touch /var/www/username_pythonanywhere_com_wsgi.py
```

### Database Commands:
```bash
# Access MySQL
mysql -u username -h username.mysql.pythonanywhere-services.com -p

# Show databases
SHOW DATABASES;

# Use database
USE username$invoicehub;

# Show tables
SHOW TABLES;
```

---

## 🎯 Post-Deployment Checklist

- [ ] App loads at username.pythonanywhere.com
- [ ] Login page works
- [ ] Can create account
- [ ] Can add clients
- [ ] Can create invoices
- [ ] PDF generation works
- [ ] Settings page works
- [ ] All pages load correctly
- [ ] No errors in error log

---

## 🆘 Need Help?

- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Documentation**: https://help.pythonanywhere.com/pages/Flask/

---

## 🎉 Success!

Your InvoiceHub is now live and accessible to anyone at:
```
https://username.pythonanywhere.com
```

Share the link and start managing invoices! 🚀✨

---

**Last Updated:** May 3, 2026
