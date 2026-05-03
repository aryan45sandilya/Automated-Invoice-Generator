#!/bin/bash

# PythonAnywhere Update Script
# Run this script to update your deployed application

echo "🔄 Pulling latest changes from GitHub..."
git pull origin main

echo "✅ Changes pulled successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click the 'Reload' button for aryansandilya.pythonanywhere.com"
echo "3. Clear your browser cache (Ctrl+Shift+Delete)"
echo "4. Refresh the website"
echo ""
echo "💡 Tip: Hard refresh with Ctrl+F5 to bypass cache"
