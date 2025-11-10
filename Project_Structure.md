# FastAPI Tourism Guide - Project Structure
"""
tourism_guide_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── destination.py
│   │   ├── category.py
│   │   ├── review.py
│   │   ├── route.py
│   │   └── feedback.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── destination.py
│   │   ├── category.py
│   │   ├── review.py
│   │   ├── route.py
│   │   └── feedback.py
│   │
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py             # Login/Register/Logout
│   │   ├── destinations.py     # Destination CRUD
│   │   ├── reviews.py          # Reviews
│   │   ├── routes.py           # Routes
│   │   └── feedback.py         # Feedback
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── destination_service.py
│   │   ├── review_service.py
│   │   └── file_service.py
│   │
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── destination.html
│   │   ├── login.html
│   │   └── feedback.html
│   │
│   ├── static/                 # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── uploads/                # Uploaded files
│       ├── destinations/
│       └── categories/
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_destinations.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
"""

# Installation Commands:
"""
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install fastapi[all] uvicorn sqlalchemy pymysql python-multipart \
            python-jose[cryptography] passlib[bcrypt] python-dotenv \
            jinja2 aiofiles alembic pillow

# Create .env file with:
DATABASE_URL=mysql+pymysql://root:@localhost/tourism_guide_fastapi
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run migrations
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""