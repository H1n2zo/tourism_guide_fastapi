from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.config import settings
from app.database import engine, Base

# Import routers

from app.routers import auth, destinations, reviews, routes_api, feedback, admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Tourism Guide System API - Explore Ormoc City",
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(reviews.router)
app.include_router(routes_api.router)
app.include_router(feedback.router)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/destination/{destination_id}", response_class=HTMLResponse)
async def destination_page(request: Request, destination_id: int):
    """Destination detail page"""
    return templates.TemplateResponse(
        "destination.html",
        {"request": request, "destination_id": destination_id}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login/Register page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/feedback-page", response_class=HTMLResponse)
async def feedback_page(request: Request):
    """Feedback page"""
    return templates.TemplateResponse("feedback.html", {"request": request})

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# API documentation info
@app.get("/api")
async def api_info():
    """API information"""
    return {
        "message": "Tourism Guide System API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)