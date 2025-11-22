"""
Route API Endpoints
CRUD operations for transportation routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from config.database import get_db
from models.route import Route
from models.destination import Destination
from schemas.route import RouteCreate, RouteUpdate, RouteResponse
from core.security import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[RouteResponse])
async def get_routes(
    origin_id: Optional[int] = None,
    destination_id: Optional[int] = None,
    transport_mode: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all routes with optional filtering
    """
    query = db.query(
        Route,
        Destination.name.label('origin_name'),
        Destination.latitude.label('origin_lat'),
        Destination.longitude.label('origin_lng')
    ).join(Destination, Route.origin_id == Destination.id)
    
    # Join destination point
    dest_query = db.query(
        Destination.name,
        Destination.latitude,
        Destination.longitude
    ).filter(Destination.id == Route.destination_id).first()
    
    # Filters
    if origin_id:
        query = query.filter(Route.origin_id == origin_id)
    
    if destination_id:
        query = query.filter(Route.destination_id == destination_id)
    
    if transport_mode:
        query = query.filter(Route.transport_mode == transport_mode)
    
    if is_active is not None:
        query = query.filter(Route.is_active == is_active)
    
    results = query.order_by(Route.route_name).all()
    
    # Format response with full details
    routes = []
    for route, origin_name, origin_lat, origin_lng in results:
        # Get destination details
        dest = db.query(Destination).filter(Destination.id == route.destination_id).first()
        
        # Calculate total fare
        total_fare = Decimal('0.00')
        if route.base_fare and route.distance_km and route.fare_per_km:
            total_fare = route.base_fare + (route.distance_km * route.fare_per_km)
        elif route.base_fare:
            total_fare = route.base_fare
        
        route_dict = {
            **route.__dict__,
            'origin_name': origin_name,
            'origin_lat': origin_lat,
            'origin_lng': origin_lng,
            'destination_name': dest.name if dest else None,
            'dest_lat': dest.latitude if dest else None,
            'dest_lng': dest.longitude if dest else None,
            'total_fare': total_fare
        }
        routes.append(route_dict)
    
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(route_id: int, db: Session = Depends(get_db)):
    """
    Get single route by ID
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    # Get origin and destination details
    origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
    destination = db.query(Destination).filter(Destination.id == route.destination_id).first()
    
    # Calculate total fare
    total_fare = Decimal('0.00')
    if route.base_fare and route.distance_km and route.fare_per_km:
        total_fare = route.base_fare + (route.distance_km * route.fare_per_km)
    elif route.base_fare:
        total_fare = route.base_fare
    
    return {
        **route.__dict__,
        'origin_name': origin.name if origin else None,
        'origin_lat': origin.latitude if origin else None,
        'origin_lng': origin.longitude if origin else None,
        'destination_name': destination.name if destination else None,
        'dest_lat': destination.latitude if destination else None,
        'dest_lng': destination.longitude if destination else None,
        'total_fare': total_fare
    }


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route: RouteCreate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create new route (Admin only)
    """
    # Verify origin and destination exist
    origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
    if not origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Origin destination not found"
        )
    
    destination = db.query(Destination).filter(Destination.id == route.destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Check if route already exists
    existing = db.query(Route).filter(
        Route.origin_id == route.origin_id,
        Route.destination_id == route.destination_id,
        Route.transport_mode == route.transport_mode
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Route with this origin, destination, and transport mode already exists"
        )
    
    # Create route
    new_route = Route(**route.dict())
    
    # Generate route name if not provided
    if not new_route.route_name:
        new_route.route_name = f"{origin.name} to {destination.name}"
    
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    
    return new_route


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: int,
    route: RouteUpdate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update route (Admin only)
    """
    db_route = db.query(Route).filter(Route.id == route_id).first()
    
    if not db_route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    # Verify destinations exist if they're being changed
    if route.origin_id:
        origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
        if not origin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Origin destination not found"
            )
    
    if route.destination_id:
        destination = db.query(Destination).filter(
            Destination.id == route.destination_id
        ).first()
        if not destination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination not found"
            )
    
    # Update fields
    for field, value in route.dict(exclude_unset=True).items():
        setattr(db_route, field, value)
    
    db.commit()
    db.refresh(db_route)
    
    return db_route


@router.delete("/{route_id}")
async def delete_route(
    route_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete route (Admin only)
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    db.delete(route)
    db.commit()
    
    return {
        "message": "Route deleted successfully",
        "success": True
    }


@router.get("/find/route")
async def find_route(
    origin_id: int,
    destination_id: int,
    transport_mode: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Find routes between two destinations
    """
    query = db.query(Route).filter(
        Route.origin_id == origin_id,
        Route.destination_id == destination_id,
        Route.is_active == True
    )
    
    if transport_mode:
        query = query.filter(Route.transport_mode == transport_mode)
    
    routes = query.all()
    
    if not routes:
        # Try reverse route
        routes = db.query(Route).filter(
            Route.origin_id == destination_id,
            Route.destination_id == origin_id,
            Route.is_active == True
        ).all()
        
        if not routes:
            return {
                "found": False,
                "message": "No route found between these destinations",
                "routes": []
            }
    
    # Format response
    formatted_routes = []
    for route in routes:
        origin = db.query(Destination).filter(Destination.id == route.origin_id).first()
        dest = db.query(Destination).filter(Destination.id == route.destination_id).first()
        
        total_fare = Decimal('0.00')
        if route.base_fare and route.distance_km and route.fare_per_km:
            total_fare = route.base_fare + (route.distance_km * route.fare_per_km)
        elif route.base_fare:
            total_fare = route.base_fare
        
        formatted_routes.append({
            **route.__dict__,
            'origin_name': origin.name if origin else None,
            'destination_name': dest.name if dest else None,
            'total_fare': float(total_fare)
        })
    
    return {
        "found": True,
        "count": len(formatted_routes),
        "routes": formatted_routes
    }


@router.get("/transport-modes/list")
async def get_transport_modes():
    """
    Get list of available transport modes
    """
    return {
        "transport_modes": [
            {"value": "jeepney", "label": "Jeepney", "icon": "fa-bus"},
            {"value": "taxi", "label": "Taxi", "icon": "fa-taxi"},
            {"value": "bus", "label": "Bus", "icon": "fa-bus-alt"},
            {"value": "van", "label": "Van", "icon": "fa-shuttle-van"},
            {"value": "tricycle", "label": "Tricycle", "icon": "fa-motorcycle"},
            {"value": "walking", "label": "Walking", "icon": "fa-walking"}
        ]
    }