# Routers package initialization
# Import all routers here for easy access

from app.routers import auth, destinations, reviews, routes_api, feedback, admin

__all__ = [
    "auth",
    "destinations", 
    "reviews",
    "routes_api",
    "feedback",
    "admin"
]