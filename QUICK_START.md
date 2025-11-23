# 🚀 Tourism Guide FastAPI - Quick Start

Get your Tourism Guide running in **5 minutes**!

---

## ⚡ Super Fast Setup

### 1. Prerequisites Check
```bash
# Check Python version (need 3.8+)
python --version

# Check MySQL is running
mysql --version
```

### 2. Clone and Setup
```bash
# Create project directory
mkdir tourism_guide_fastapi
cd tourism_guide_fastapi

# Run setup script
python setup.py
```

### 3. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Run these commands
CREATE DATABASE tourism_guide;
USE tourism_guide;
SOURCE tourism_guide.sql;
EXIT;
```

### 5. Configure Environment
```bash
# Edit .env file - update if needed:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/tourism_guide
```

### 6. Run Application
```bash
uvicorn main:app --reload
```

### 7. Access System
- **Homepage**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Admin Panel**: http://localhost:8000/admin
- **Login**: `admin` / `admin123`

---

## 📂 File Checklist

Make sure you have all these files:

### Core Files
- ✅ `main.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `.env` - Configuration
- ✅ `setup.py` - Setup script
- ✅ `README.md` - Documentation

### Config Files
- ✅ `config/database.py`
- ✅ `config/settings.py`

### Models
- ✅ `models/__init__.py`
- ✅ All model files (user, destination, etc.)

### Schemas
- ✅ `schemas/__init__.py`
- ✅ All schema files (user, destination, etc.)

### API Endpoints
- ✅ `api/endpoints/auth.py`
- ✅ `api/endpoints/destinations.py`
- ✅ `api/endpoints/categories.py`
- ✅ `api/endpoints/reviews.py`
- ✅ `api/endpoints/routes.py`
- ✅ `api/endpoints/feedback.py`
- ✅ `api/endpoints/admin.py`

### Core
- ✅ `core/security.py`
- ✅ `core/utils.py`

### Templates (HTML)
- ✅ `templates/index.html`
- ✅ `templates/login.html`
- ✅ `templates/destination.html`
- ✅ `templates/feedback.html`
- ✅ `templates/admin/*.html`

---

## 🐛 Common Issues & Fixes

### Issue: "ModuleNotFoundError"
```bash
# Solution: Activate virtual environment
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Can't connect to MySQL"
```bash
# Solution: Check MySQL is running and credentials
# Update .env file with correct password
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/tourism_guide
```

### Issue: "Port 8000 already in use"
```bash
# Solution: Use different port
uvicorn main:app --reload --port 8001
```

### Issue: "No such file or directory: templates"
```bash
# Solution: Create templates directory
mkdir templates
mkdir templates/admin
```

### Issue: "ImportError: No module named PIL"
```bash
# Solution: Install Pillow
pip install Pillow
```

---

## 🔑 Default Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`
- Email: `admin@tourismguide.com`

**⚠️ CHANGE THESE IMMEDIATELY AFTER FIRST LOGIN!**

---

## 📊 Verify Installation

Run these commands to test:

```bash
# Test API
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "app": "Tourism Guide System",
#   "version": "2.0.0",
#   "map_provider": "OpenStreetMap (FREE)"
# }
```

### Test in Browser
1. Visit http://localhost:8000
2. Should see homepage with map
3. Visit http://localhost:8000/api/docs
4. Should see interactive API documentation

---

## 🎯 Quick Commands

### Development
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run on specific port
uvicorn main:app --reload --port 8001

# Run with debug logs
uvicorn main:app --reload --log-level debug
```

### Database
```bash
# Export database
mysqldump -u root -p tourism_guide > backup.sql

# Import database
mysql -u root -p tourism_guide < backup.sql

# Reset database
mysql -u root -p -e "DROP DATABASE tourism_guide; CREATE DATABASE tourism_guide;"
mysql -u root -p tourism_guide < tourism_guide.sql
```

### Virtual Environment
```bash
# Activate
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Deactivate
deactivate

# Update packages
pip install --upgrade -r requirements.txt
```

---

## 🗺️ Free Mapping Features

### What Works Out of the Box
- ✅ Interactive maps (OpenStreetMap)
- ✅ Destination markers
- ✅ Route visualization
- ✅ Distance calculation
- ✅ Fare estimation
- ✅ GPS location detection

### No Setup Required
- ❌ NO API keys
- ❌ NO credit cards
- ❌ NO registration
- ❌ NO usage limits
- ❌ NO monthly bills

**Just works! 🎉**

---

## 📱 Testing the System

### 1. Test Homepage
```
Visit: http://localhost:8000
✓ Map loads
✓ Destinations appear
✓ Search works
✓ Filters work
```

### 2. Test Login
```
Visit: http://localhost:8000/login
✓ Login with admin/admin123
✓ Redirects to admin panel
```

### 3. Test Admin Panel
```
Visit: http://localhost:8000/admin
✓ Dashboard shows stats
✓ Can add destinations
✓ Can manage categories
✓ Can view routes
```

### 4. Test API
```
Visit: http://localhost:8000/api/docs
✓ Swagger UI loads
✓ Can test endpoints
✓ Authentication works
```

---

## 🚀 Next Steps

After successful setup:

1. **Customize**: Edit templates to match your brand
2. **Add Data**: Import your destinations via admin panel
3. **Test**: Try all features thoroughly
4. **Deploy**: Follow deployment guide in README.md
5. **Monitor**: Check logs and performance

---

## 💡 Pro Tips

### Performance
- Use `--workers 4` for production
- Enable database connection pooling
- Optimize images before uploading

### Security
- Change SECRET_KEY in production
- Use strong admin password
- Enable HTTPS
- Keep dependencies updated

### Development
- Use `--reload` during development
- Check `/api/docs` for API testing
- Monitor logs for errors
- Test on mobile devices

---

## 📞 Need Help?

### Resources
- 📚 Full documentation: README.md
- 🔧 API docs: http://localhost:8000/api/docs
- 🗺️ OpenStreetMap: https://www.openstreetmap.org
- 🍃 Leaflet: https://leafletjs.com

### Common Questions

**Q: Can I use a different database?**
A: Yes! FastAPI supports PostgreSQL, SQLite, etc. Update DATABASE_URL in .env

**Q: Do I need API keys?**
A: No! We use OpenStreetMap which is 100% free forever.

**Q: Can I deploy this?**
A: Yes! Works with Heroku, Railway, DigitalOcean, AWS, etc.

**Q: Is this production-ready?**
A: Yes, but remember to change SECRET_KEY and admin credentials!

---

## ✅ Success Checklist

Before going live, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Database created and imported
- [ ] .env file configured
- [ ] Application starts without errors
- [ ] Homepage loads correctly
- [ ] Maps display properly
- [ ] Login works
- [ ] Admin panel accessible
- [ ] Can add/edit destinations
- [ ] Routes display correctly
- [ ] API documentation works
- [ ] Changed admin password
- [ ] Updated SECRET_KEY

---

**🎉 You're all set! Enjoy your FREE Tourism Guide System!**

Made with ❤️ using FastAPI, Python, and OpenStreetMap