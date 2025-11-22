# Tourism Guide FastAPI - Complete Project Structure

## 📁 Project Directory Structure

```
tourism_guide_fastapi/
├── main.py                          # Main FastAPI application
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables
├── README.md                       # Project documentation
│
├── config/
│   ├── __init__.py
│   ├── database.py                 # Database configuration
│   └── settings.py                 # App settings
│
├── models/
│   ├── __init__.py
│   ├── user.py                     # User model
│   ├── destination.py              # Destination model
│   ├── category.py                 # Category model
│   ├── review.py                   # Review model
│   ├── route.py                    # Route model
│   └── feedback.py                 # Feedback model
│
├── schemas/
│   ├── __init__.py
│   ├── user.py                     # User schemas (Pydantic)
│   ├── destination.py              # Destination schemas
│   ├── category.py                 # Category schemas
│   ├── review.py                   # Review schemas
│   ├── route.py                    # Route schemas
│   └── feedback.py                 # Feedback schemas
│
├── api/
│   ├── __init__.py
│   ├── deps.py                     # Dependencies (auth, db session)
│   └── endpoints/
│       ├── __init__.py
│       ├── auth.py                 # Login, register, logout
│       ├── destinations.py         # Destination CRUD
│       ├── categories.py           # Category CRUD
│       ├── reviews.py              # Review CRUD
│       ├── routes.py               # Route CRUD
│       ├── feedback.py             # Feedback CRUD
│       └── admin.py                # Admin operations
│
├── core/
│   ├── __init__.py
│   ├── security.py                 # Password hashing, JWT tokens
│   └── utils.py                    # Helper functions
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── uploads/
│   ├── destinations/
│   └── categories/
│
└── templates/
    ├── index.html                  # Homepage
    ├── login.html                  # Login page
    ├── destination.html            # Destination detail
    ├── feedback.html               # Feedback page
    └── admin/
        ├── dashboard.html
        ├── destinations.html
        ├── add_destination.html
        ├── categories.html
        ├── routes.html
        └── users.html
```

## 📦 Installation Steps

### 1. Create Project Directory
```bash
mkdir tourism_guide_fastapi
cd tourism_guide_fastapi
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE tourism_guide;
exit;

# Run migrations (auto-creates tables)
python main.py
```

### 5. Create .env File
```bash
# Copy and edit .env file with your settings
cp .env.example .env
```

### 6. Run Application
```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access at: http://localhost:8000
```

## 🚀 Key Features

### ✅ Converted from PHP
- User authentication (JWT-based)
- Destination management
- Category management
- Review system
- Route planning
- Feedback system
- Admin dashboard
- Image uploads
- OpenStreetMap integration

### ✅ FastAPI Advantages
- **Async/Await** - Better performance
- **Type Safety** - Pydantic validation
- **Auto Documentation** - Swagger UI at `/docs`
- **Modern Python** - Python 3.8+
- **Dependency Injection** - Clean architecture
- **Security** - Built-in CORS, OAuth2

## 🔧 Configuration

### Environment Variables (.env)
```
DATABASE_URL=mysql+pymysql://root:@localhost/tourism_guide
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880
```

## 📚 API Documentation

After running the app, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Default Admin Login

```
Username: admin
Password: admin123
```

## 🗺️ Free Mapping Features

- OpenStreetMap (No API key needed!)
- Leaflet.js integration
- Route calculation
- Distance estimation
- Fare calculation
- GPS location detection

## 📝 Next Steps

1. Create all Python files following the structure above
2. Copy HTML templates (keep Leaflet/OpenStreetMap code)
3. Test all endpoints via `/docs`
4. Deploy using Docker or Heroku

## 🔄 Migration from PHP

| PHP Component | FastAPI Equivalent |
|--------------|-------------------|
| `$_SESSION` | JWT tokens |
| `mysqli` | SQLAlchemy ORM |
| `password_verify()` | `passlib` + `bcrypt` |
| `header('Location:')` | `RedirectResponse` |
| `$_POST`, `$_GET` | Pydantic models |
| `move_uploaded_file()` | `UploadFile` |

## 🎯 Performance Benefits

- **5-10x faster** than PHP
- Async database queries
- Better concurrency
- Lower memory usage
- Type safety catches bugs early

---

**Ready to start?** Let's create each file! 🚀