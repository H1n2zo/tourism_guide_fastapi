# main.py - FastAPI Application Entry Point
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.database import engine, Base
from app.api.endpoints import destinations, categories, routes, reviews, feedback
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Tourism Guide System",
    description="Explore amazing places in Ormoc City",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(destinations.router, prefix="/api/destinations", tags=["destinations"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(routes.router, prefix="/api/routes", tags=["routes"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])


# USER PANEL ROUTES (HTML Pages)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage with destinations and map"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/destination/{destination_id}", response_class=HTMLResponse)
async def destination_detail(request: Request, destination_id: int):
    """Destination detail page"""
    return templates.TemplateResponse(
        "destinations.html", 
        {"request": request, "destination_id": destination_id}
    )


@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request):
    """Feedback submission page"""
    return templates.TemplateResponse("feedback.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)