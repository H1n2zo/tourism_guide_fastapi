# FastAPI Tourism Guide - Installation Guide

## Prerequisites
- Python 3.8 or higher
- MySQL/MariaDB server
- XAMPP (recommended) or standalone MySQL

## Step 1: Clone/Download the Project
```bash
git clone https://github.com/H1n2zo/tourism_guide_fastapi
cd tourism_guide_fastapi
```

## Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Setup Database

### Option A: Using XAMPP
1. Start XAMPP Control Panel
2. Start Apache and MySQL
3. Open phpMyAdmin (http://localhost/phpmyadmin)
4. Create database: `tourism_guide_fastapi`
5. Import the SQL file: `tourism_guide.sql`

### Option B: Using MySQL Command Line
```bash
mysql -u root -p
CREATE DATABASE tourism_guide_fastapi;
USE tourism_guide_fastapi;
SOURCE tourism_guide.sql;
EXIT;
```

## Step 5: Configure Environment Variables

Create `.env` file in the project root:
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost/tourism_guide_fastapi

# Security Settings
SECRET_KEY=your-secret-key-change-in-production-09af9s0d8f7asd098f7a
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
APP_NAME=Tourism Guide System
APP_VERSION=1.0.0
DEBUG=True

# File Upload Settings
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# CORS Settings (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000
```

## Step 6: Create Upload Directories
```bash
# Windows
mkdir uploads
mkdir uploads\destinations
mkdir uploads\categories

# Linux/Mac
mkdir -p uploads/destinations
mkdir -p uploads/categories
```

## Step 7: Run Database Migrations (Optional)
```bash
# Initialize Alembic (if not done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Step 8: Run the Application
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Step 9: Access the Application

### Public Pages
- Homepage: http://localhost:8000
- Destinations: http://localhost:8000/#destinations
- Routes: http://localhost:8000/#routes
- Feedback: http://localhost:8000/feedback-page
- Login: http://localhost:8000/login

### Admin Panel
- Dashboard: http://localhost:8000/admin/dashboard
- Manage Destinations: http://localhost:8000/admin/destinations
- Manage Categories: http://localhost:8000/admin/categories
- Manage Routes: http://localhost:8000/admin/routes
- Reviews & Feedback: http://localhost:8000/admin/reviews
- Manage Users: http://localhost:8000/admin/users

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Step 10: Create Admin User

### Option A: Using phpMyAdmin
1. Go to http://localhost/phpmyadmin
2. Select `tourism_guide_fastapi` database
3. Open the `users` table
4. Find your user and change `role` from `user` to `admin`

### Option B: Register and Update
1. Register at http://localhost:8000/login
2. Update user role in database:
```sql
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

## Default Login Credentials
After importing the SQL file:
- Username: `Admin`
- Password: `admin123`

**⚠️ Change this password immediately after first login!**

## Project Structure
```
tourism_guide_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── dependencies.py      # Auth dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── destinations.py
│   │   ├── reviews.py
│   │   ├── routes_api.py
│   │   ├── feedback.py
│   │   └── admin.py         # Admin endpoints
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   └── file_service.py
│   ├── templates/           # Jinja2 templates
│   │   ├── admin/           # Admin panel templates
│   │   └── *.html           # Public templates
│   └── static/              # Static files
├── uploads/                 # User uploads
├── alembic/                 # Database migrations
├── requirements.txt
├── .env
└── README.md
```

## Troubleshooting

### Database Connection Error
```
Error: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```
**Solution:** 
- Make sure MySQL is running in XAMPP
- Check DATABASE_URL in .env file
- Verify database name exists

### Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Upload Directory Error
```
FileNotFoundError: [Errno 2] No such file or directory: 'uploads/destinations'
```
**Solution:**
```bash
mkdir -p uploads/destinations uploads/categories
```

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution:**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Import Error
```
ImportError: cannot import name 'get_current_admin'
```
**Solution:** Make sure all files are in correct locations and dependencies.py exists

## Features

### User Features
✅ Browse destinations with ratings
✅ View destination details with maps
✅ Find routes between locations
✅ Submit reviews and feedback
✅ User registration and login

### Admin Features
✅ Dashboard with statistics
✅ Manage destinations (CRUD)
✅ Manage categories
✅ Manage routes
✅ Review management
✅ Feedback management
✅ User management
✅ Image upload
✅ Real-time stats

### Technical Features
✅ RESTful API
✅ JWT Authentication
✅ Role-based access control
✅ File upload handling
✅ OpenStreetMap integration (FREE)
✅ Responsive design
✅ API documentation (Swagger/ReDoc)

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login
- GET `/api/auth/me` - Get current user
- POST `/api/auth/logout` - Logout

### Destinations
- GET `/api/destinations/` - List all destinations
- GET `/api/destinations/{id}` - Get destination details
- GET `/api/destinations/categories` - List categories
- GET `/api/destinations/statistics/summary` - Get statistics

### Reviews
- POST `/api/reviews/` - Submit review
- GET `/api/reviews/destination/{id}` - Get destination reviews

### Routes
- GET `/api/routes/` - List all routes
- GET `/api/routes/{id}` - Get route details

### Feedback
- POST `/api/feedback/` - Submit feedback
- GET `/api/feedback/public` - Get public feedback
- GET `/api/feedback/statistics` - Get statistics

### Admin (Requires Authentication)
- GET `/api/admin/dashboard/stats` - Dashboard statistics
- POST `/api/admin/destinations` - Create destination
- PUT `/api/admin/destinations/{id}` - Update destination
- DELETE `/api/admin/destinations/{id}` - Delete destination
- POST `/api/admin/categories` - Create category
- POST `/api/admin/routes` - Create route
- DELETE `/api/admin/reviews/{id}` - Delete review
- PUT `/api/admin/feedback/{id}/read` - Mark feedback as read

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
# Format code
black app/

# Check linting
flake8 app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables
Update `.env` for production:
```env
DEBUG=False
SECRET_KEY=<strong-random-secret-key>
DATABASE_URL=mysql+pymysql://user:password@host/database
ALLOWED_ORIGINS=https://yourdomain.com
```

### Security Checklist
- [ ] Change SECRET_KEY
- [ ] Change default admin password
- [ ] Set DEBUG=False
- [ ] Configure CORS properly
- [ ] Use HTTPS
- [ ] Set up firewall rules
- [ ] Regular database backups
- [ ] Update dependencies regularly

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check GitHub issues
4. Contact project maintainers

## License

MIT License - See LICENSE file for details

## Credits

- FastAPI Framework
- OpenStreetMap & Leaflet (Free mapping)
- Bootstrap 5
- Font Awesome Icons

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Python:** 3.8+  
**Database:** MySQL/MariaDB