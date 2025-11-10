from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.route import Route, TransportMode
from app.models.destination import Destination
from app.schemas.route import RouteResponse

router = APIRouter(prefix="/api/routes", tags=["Routes"])

@router.get("/", response_model=List[RouteResponse])
def get_routes(
    transport_mode: Optional[TransportMode] = Query(None, description="Filter by transport mode"),
    origin_id: Optional[int] = Query(None, description="Filter by origin"),
    destination_id: Optional[int] = Query(None, description="Filter by destination"),
    is_active: bool = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all routes with optional filters"""
    query = db.query(
        Route,
        Destination.name.label('origin_name'),
        Destination.latitude.label('origin_lat'),
        Destination.longitude.label('origin_lng'),
        Destination.name.label('destination_name'),
        Destination.latitude.label('dest_lat'),
        Destination.longitude.label('dest_lng')
    ).join(
        Destination, Route.origin_id == Destination.id, isouter=True
    ).join(
        Destination, Route.destination_id == Destination.id, isouter=True
    ).filter(
        Route.is_active == is_active
    )
    
    if transport_mode:
        query = query.filter(Route.transport_mode == transport_mode)
    
    if origin_id:
        query = query.filter(Route.origin_id == origin_id)
    
    if destination_id:
        query = query.filter(Route.destination_id == destination_id)
    
    query = query.order_by(Route.created_at.desc())
    
    routes = query.offset(skip).limit(limit).all()
    
    # Format response
    result = []
    for route, origin_name, origin_lat, origin_lng, dest_name, dest_lat, dest_lng in routes:
        total_fare = (route.base_fare or 0) + ((route.distance_km or 0) * (route.fare_per_km or 0))
        
        result.append({
            "id": route.id,
            "route_name": route.route_name,
            "origin_id": route.origin_id,
            "destination_id": route.destination_id,
            "transport_mode": route.transport_mode,
            "distance_km": route.distance_km,
            "estimated_time_minutes": route.estimated_time_minutes,
            "base_fare": route.base_fare,
            "fare_per_km": route.fare_per_km,
            "description": route.description,
            "is_active": route.is_active,
            "created_at": route.created_at,
            "origin_name": origin_name,
            "destination_name": dest_name,
            "origin_lat": origin_lat,
            "origin_lng": origin_lng,
            "dest_lat": dest_lat,
            "dest_lng": dest_lng,
            "total_fare": float(total_fare)
        })
    
    return result

@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    db: Session = Depends(get_db)
):
    """Get route by ID"""
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Get origin and destination names
    origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
    destination = db.query(Destination).filter(Destination.id == route.destination_id).first()
    
    total_fare = (route.base_fare or 0) + ((route.distance_km or 0) * (route.fare_per_km or 0))
    
    return {
        **route.__dict__,
        "origin_name": origin.name if origin else None,
        "destination_name": destination.name if destination else None,
        "origin_lat": origin.latitude if origin else None,
        "origin_lng": origin.longitude if origin else None,
        "dest_lat": destination.latitude if destination else None,
        "dest_lng": destination.longitude if destination else None,
        "total_fare": float(total_fare)
    }