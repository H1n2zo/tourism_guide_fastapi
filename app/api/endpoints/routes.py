# app/api/endpoints/routes.py - Route API Endpoints (FIXED)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app.database import get_db
from app.models.route import Route
from app.models.destination import Destination
from app.schemas.route import RouteResponse

router = APIRouter()


@router.get("/", response_model=List[RouteResponse])
def get_routes(
    origin_id: Optional[int] = None,
    destination_id: Optional[int] = None,
    transport_mode: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get all routes with optional filters"""
    
    query = db.query(Route).filter(Route.is_active == is_active)
    
    # Apply filters
    if origin_id:
        query = query.filter(Route.origin_id == origin_id)
    
    if destination_id:
        query = query.filter(Route.destination_id == destination_id)
    
    if transport_mode:
        query = query.filter(Route.transport_mode == transport_mode)
    
    routes = query.order_by(Route.route_name).all()
    
    # Enrich with destination data
    result_routes = []
    for route in routes:
        origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
        destination = db.query(Destination).filter(Destination.id == route.destination_id).first()
        
        # Calculate total fare safely
        total_fare = None
        if route.base_fare is not None and route.distance_km is not None and route.fare_per_km is not None:
            total_fare = Decimal(str(route.base_fare)) + (Decimal(str(route.distance_km)) * Decimal(str(route.fare_per_km)))
        
        route_data = {
            **route.__dict__,
            'origin_name': origin.name if origin else None,
            'destination_name': destination.name if destination else None,
            'origin_lat': origin.latitude if origin else None,
            'origin_lng': origin.longitude if origin else None,
            'dest_lat': destination.latitude if destination else None,
            'dest_lng': destination.longitude if destination else None,
            'total_fare': total_fare
        }
        result_routes.append(RouteResponse(**route_data))
    
    return result_routes


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    """Get single route by ID"""
    
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
    destination = db.query(Destination).filter(Destination.id == route.destination_id).first()
    
    # Calculate total fare safely
    total_fare = None
    if route.base_fare is not None and route.distance_km is not None and route.fare_per_km is not None:
        total_fare = Decimal(str(route.base_fare)) + (Decimal(str(route.distance_km)) * Decimal(str(route.fare_per_km)))
    
    route_data = {
        **route.__dict__,
        'origin_name': origin.name if origin else None,
        'destination_name': destination.name if destination else None,
        'origin_lat': origin.latitude if origin else None,
        'origin_lng': origin.longitude if origin else None,
        'dest_lat': destination.latitude if destination else None,
        'dest_lng': destination.longitude if destination else None,
        'total_fare': total_fare
    }
    
    return RouteResponse(**route_data)