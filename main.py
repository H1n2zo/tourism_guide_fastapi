"""
Tourism Guide FastAPI - Main Application
Free Version with OpenStreetMap (No API Keys Required!)
"""

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os

from config.database import engine, Base, get_db
from config.settings import settings
from api.endpoints import auth, destinations, categories, reviews, routes, feedback, admin
from core.security import create_default_admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Tourism Guide System with OpenStreetMap (100% Free!)",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
os.makedirs("static", exist_ok=True)
os.makedirs("uploads/destinations", exist_ok=True)
os.makedirs("uploads/categories", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(destinations.router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Homepage with destinations and map"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "settings": settings}
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login and registration page"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "settings": settings}
    )


@app.get("/destination/{destination_id}", response_class=HTMLResponse)
async def destination_detail(request: Request, destination_id: int):
    """Destination detail page"""
    return templates.TemplateResponse(
        "destination.html",
        {"request": request, "destination_id": destination_id, "settings": settings}
    )


@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request):
    """Feedback page"""
    return templates.TemplateResponse(
        "feedback.html",
        {"request": request, "settings": settings}
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect():
    """Redirect to admin dashboard"""
    return RedirectResponse(url="/admin/dashboard")


@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard"""
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "settings": settings}
    )


@app.get("/admin/destinations", response_class=HTMLResponse)
async def admin_destinations(request: Request):
    """Admin destinations management"""
    return templates.TemplateResponse(
        "admin/destinations.html",
        {"request": request, "settings": settings}
    )


@app.get("/admin/categories", response_class=HTMLResponse)
async def admin_categories(request: Request):
    """Admin categories management"""
    return templates.TemplateResponse(
        "admin/categories.html",
        {"request": request, "settings": settings}
    )


@app.get("/admin/routes", response_class=HTMLResponse)
async def admin_routes(request: Request):
    """Admin routes management"""
    return templates.TemplateResponse(
        "admin/routes.html",
        {"request": request, "settings": settings}
    )


@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users(request: Request):
    """Admin users management"""
    return templates.TemplateResponse(
        "admin/users.html",
        {"request": request, "settings": settings}
    )


@app.on_event("startup")
async def startup_event():
    """Create default admin user on startup"""
    db = next(get_db())
    create_default_admin(db)
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║  🎉 Tourism Guide FastAPI - Started Successfully! 🎉  ║
    ╠════════════════════════════════════════════════════════╣
    ║  📍 Homepage:      http://localhost:8000               ║
    ║  📚 API Docs:      http://localhost:8000/api/docs      ║
    ║  🔐 Admin Login:   admin / admin123                    ║
    ║  🗺️  Free Maps:     OpenStreetMap (No API Key!)       ║
    ╚════════════════════════════════════════════════════════╝
    """)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "map_provider": "OpenStreetMap (FREE)"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )