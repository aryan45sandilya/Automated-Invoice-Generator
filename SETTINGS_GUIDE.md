# ⚙️ Company Settings Guide

## ✅ Settings Feature Added!

Ab aap apni company ki saari details easily change kar sakte ho!

---

## 🎯 Kaise Use Karein

### **Step 1: Settings Page Kholein**
1. Login karein: http://localhost:5000
2. Sidebar mein **"Settings"** par click karein
3. Ya directly jaayein: http://localhost:5000/settings/

### **Step 2: Company Details Update Karein**

#### **Company Information**
- **Company Name** - Aapki company ka naam (Invoice par dikhega)
- **Company Email** - Official email address
- **Company Phone** - Contact number (+91-XXXXX-XXXXX)
- **Company Address** - Complete address with PIN code

#### **Currency & Tax Settings**
- **Currency Symbol** - ₹ (Rupee), $ (Dollar), € (Euro), £ (Pound)
- **Currency Code** - INR, USD, EUR, GBP
- **Default Tax Rate** - GST rate (5%, 12%, 18%, 28%)
- **Invoice Prefix** - Invoice number prefix (INV, BILL, etc.)

### **Step 3: Save Settings**
1. Saari details fill karein
2. **"Save Settings"** button click karein
3. Success message dikhega

### **Step 4: Application Restart Karein**
Settings apply karne ke liye:
1. Terminal mein **Ctrl + C** press karein
2. Phir se run karein: `python app.py`
3. Browser refresh karein

---

## 📋 Example Settings

### **For Indian Company:**
```
Company Name: Tech Solutions Pvt Ltd
Company Email: info@techsolutions.in
Company Phone: +91-98765-43210
Company Address: 123 Business Park, Mumbai, Maharashtra, 400001, India

Currency Symbol: ₹
Currency Code: INR
Default Tax Rate: 18.0
Invoice Prefix: INV
```

### **For US Company:**
```
Company Name: Tech Solutions Inc
Company Email: info@techsolutions.com
Company Phone: +1-555-123-4567
Company Address: 123 Business Ave, New York, NY 10001, USA

Currency Symbol: $
Currency Code: USD
Default Tax Rate: 10.0
Invoice Prefix: INV
```

---

## 🎨 Kya Kya Change Hoga

### **After Updating Settings:**

1. **Dashboard** - Company name updated
2. **Invoices** - New currency symbol
3. **PDFs** - Company details updated
4. **Emails** - Company info updated
5. **Sidebar** - Company name displayed

---

## 💡 Pro Tips

### **Company Name**
- Professional naam use karein
- "Pvt Ltd", "Inc", "LLC" add karein
- Example: "ABC Technologies Pvt Ltd"

### **Currency Symbol**
- India: ₹ (INR)
- USA: $ (USD)
- Europe: € (EUR)
- UK: £ (GBP)

### **Tax Rate**
**India GST Rates:**
- 5% - Essential goods
- 12% - Standard goods
- 18% - Most services (default)
- 28% - Luxury items

**Other Countries:**
- USA: 0-10% (varies by state)
- UK: 20% VAT
- EU: 15-27% VAT

### **Invoice Prefix**
- **INV** - Invoice
- **BILL** - Bill
- **EST** - Estimate
- **QUO** - Quotation

---

## 🔧 Troubleshooting

### **Settings Not Updating?**
1. Check if you clicked "Save Settings"
2. Restart the application
3. Clear browser cache (Ctrl + Shift + R)

### **Currency Symbol Not Showing?**
1. Make sure you saved settings
2. Restart application
3. Refresh browser (Ctrl + F5)

### **Error While Saving?**
1. Check all required fields are filled
2. Make sure tax rate is between 0-100
3. Check .env file permissions

---

## 📱 Access Settings

### **From Sidebar:**
Click on **"Settings"** icon (⚙️)

### **Direct URL:**
http://localhost:5000/settings/

---

## ✅ Features

- ✅ **Easy to Use** - Simple form interface
- ✅ **Real-time Update** - Changes reflect immediately
- ✅ **Validation** - Prevents invalid data
- ✅ **Tips Included** - Helpful hints on the page
- ✅ **Safe** - Saves to .env file securely

---

## 🎯 What You Can Customize

### **Company Details**
- ✅ Company Name
- ✅ Email Address
- ✅ Phone Number
- ✅ Full Address

### **Financial Settings**
- ✅ Currency Symbol
- ✅ Currency Code
- ✅ Tax Rate (GST)
- ✅ Invoice Prefix

### **Coming Soon**
- 🔜 Company Logo Upload
- 🔜 Email Signature
- 🔜 Invoice Template Selection
- 🔜 Color Theme Customization

---

## 🚀 Quick Start

1. **Login** → http://localhost:5000
2. **Click Settings** → Sidebar mein ⚙️ icon
3. **Update Details** → Apni company ki info dalein
4. **Save** → "Save Settings" button click karein
5. **Restart** → Application restart karein
6. **Done!** → Aapki company details updated!

---

**🎊 Ab aap apni company ki details easily manage kar sakte ho!**

---

*Updated: 2026-05-03*
*Feature: Company Settings*
*Status: Active*
