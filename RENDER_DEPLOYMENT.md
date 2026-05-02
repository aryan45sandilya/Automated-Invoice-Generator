# 🚀 Render Deployment Guide

## ✅ Files Ready for Deployment

All necessary files have been created:
- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script
- ✅ `Procfile` - Process file
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies (with gunicorn & psycopg2)

---

## 📋 Step-by-Step Deployment

### Step 1: Push New Files to GitHub

```bash
git add render.yaml build.sh Procfile runtime.txt RENDER_DEPLOYMENT.md
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create Render Account

1. Go to [Render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with **GitHub** (recommended)
4. Authorize Render to access your GitHub repositories

### Step 3: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Find and select: `Automated-Invoice-Generator`
   - Click **"Connect"**

### Step 4: Configure Web Service

Fill in the following details:

**Basic Settings:**
- **Name**: `invoicehub` (or any name you prefer)
- **Region**: Choose closest to you (e.g., Singapore, Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave blank (or `invoice_management_system` if needed)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

**Instance Type:**
- Select **"Free"** plan

### Step 5: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

```bash
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=your-email@example.com
COMPANY_PHONE=+91-XXXXX-XXXXX
COMPANY_ADDRESS=Your Company Address
CURRENCY_SYMBOL=₹
CURRENCY_CODE=INR
DEFAULT_TAX_RATE=18.0
INVOICE_PREFIX=INV
```

**Important:** Generate a strong SECRET_KEY:
```python
# Run this in Python to generate:
import secrets
print(secrets.token_hex(32))
```

### Step 6: Create PostgreSQL Database (Optional but Recommended)

1. Click **"New +"** → **"PostgreSQL"**
2. **Name**: `invoicehub-db`
3. **Database**: `invoicehub`
4. **User**: `invoicehub_user`
5. **Region**: Same as web service
6. **Plan**: **Free**
7. Click **"Create Database"**

### Step 7: Connect Database to Web Service

1. Go to your Web Service dashboard
2. Click **"Environment"** tab
3. Add new environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Copy from PostgreSQL dashboard → **"Internal Database URL"**

### Step 8: Deploy!

1. Click **"Create Web Service"** button
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

---

## 🎉 After Successful Deployment

### Your App URL:
```
https://invoicehub.onrender.com
```
(Replace `invoicehub` with your service name)

### Initialize Database:

If using PostgreSQL, you need to initialize the database:

1. Go to your Web Service dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python init_db.py
   ```

---

## 🔧 Troubleshooting

### Issue: Build Failed

**Check:**
- All files are pushed to GitHub
- `requirements.txt` is correct
- Python version is compatible

**Solution:**
```bash
# Check logs in Render dashboard
# Fix issues and push again
git add .
git commit -m "Fix deployment issues"
git push origin main
```

### Issue: Application Error

**Check:**
- Environment variables are set correctly
- DATABASE_URL is correct
- SECRET_KEY is set

**Solution:**
- Check logs in Render dashboard
- Verify all environment variables

### Issue: Database Connection Error

**Check:**
- PostgreSQL database is created
- DATABASE_URL is correct (use Internal URL)
- Database is in same region

**Solution:**
```bash
# In Render Shell, test connection:
python -c "from app import db; db.create_all(); print('Database connected!')"
```

### Issue: Static Files Not Loading

**Check:**
- CSS/JS paths are correct
- Files are in `static/` folder

**Solution:**
- Render serves static files automatically
- Check browser console for errors

---

## 🔄 Auto-Deploy Setup

Render automatically deploys when you push to GitHub!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render will automatically deploy! 🚀
```

---

## ⚙️ Important Settings

### Free Tier Limitations:
- ⚠️ **Sleeps after 15 minutes** of inactivity
- ⚠️ Takes **30-50 seconds** to wake up
- ✅ 750 hours/month free
- ✅ 100 GB bandwidth/month

### Keep App Awake (Optional):
Use a service like [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes.

### Custom Domain (Optional):
1. Go to Web Service → **"Settings"**
2. Click **"Custom Domain"**
3. Add your domain
4. Update DNS records as shown

---

## 📊 Monitoring

### View Logs:
1. Go to Web Service dashboard
2. Click **"Logs"** tab
3. See real-time logs

### View Metrics:
1. Click **"Metrics"** tab
2. See CPU, Memory, Bandwidth usage

---

## 🔐 Security Checklist

Before going live:

- ✅ Change SECRET_KEY to strong random value
- ✅ Set DEBUG=False
- ✅ Use PostgreSQL (not SQLite)
- ✅ Enable HTTPS (automatic on Render)
- ✅ Set strong passwords for demo accounts
- ✅ Configure email settings
- ✅ Review environment variables

---

## 🎯 Quick Commands Reference

### Push to GitHub:
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Check Deployment Status:
- Go to Render dashboard
- Check "Events" tab

### View Live App:
```
https://your-service-name.onrender.com
```

### Access Shell:
- Render Dashboard → Shell tab
- Run Python commands

---

## 💡 Pro Tips

1. **Use PostgreSQL**: SQLite doesn't work well on Render
2. **Monitor Logs**: Check logs regularly for errors
3. **Set Up Alerts**: Enable email notifications in Render
4. **Use Environment Variables**: Never hardcode secrets
5. **Test Locally First**: Always test before pushing

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: Create issue in your repo

---

## ✅ Deployment Checklist

Before deploying:

- [ ] All files pushed to GitHub
- [ ] `render.yaml` configured
- [ ] `requirements.txt` has all dependencies
- [ ] Environment variables prepared
- [ ] SECRET_KEY generated
- [ ] Company details ready
- [ ] Email settings configured (optional)

After deploying:

- [ ] Check deployment logs
- [ ] Initialize database
- [ ] Test login functionality
- [ ] Create test invoice
- [ ] Test PDF generation
- [ ] Test email sending (if configured)
- [ ] Check all pages load correctly

---

## 🎉 Ready to Deploy!

Follow the steps above and your app will be live in 10-15 minutes!

**Your deployment URL will be:**
```
https://your-service-name.onrender.com
```

Good luck! 🚀✨
