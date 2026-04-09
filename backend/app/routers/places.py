from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_session
from app.models import Place, Prediction, Checkin
from app.services.prediction_engine import compute_prediction_for_place
from app.services import osm_service

router = APIRouter(prefix="/places", tags=["places"])

@router.get("/search")
def search_places(query: str, lat: Optional[float] = None, lng: Optional[float] = None, session: Session = Depends(get_session)):
    results = osm_service.search_osm_places(query, lat, lng)
    return results

@router.get("/location/reverse")
def reverse_geocode_location(lat: float, lng: float):
    # Returns {city, state, country} dict
    return osm_service.reverse_geocode(lat, lng)

@router.get("/nearby")
def get_nearby(lat: float, lng: float, category: str = "", radius_km: float = 10.0, session: Session = Depends(get_session)):
    results = osm_service.get_nearby_osm_places(lat, lng, category, radius_km=radius_km)
    return results

@router.get("/popular")
def get_popular(city: Optional[str] = None, country: Optional[str] = None, session: Session = Depends(get_session)):
    # Very simple popular logic based on checkin count in the last 24 hours
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    
    statement = select(Place).join(Checkin).where(Checkin.timestamp >= yesterday)
    if city:
        statement = statement.where(Place.city == city)
    if country:
        statement = statement.where(Place.country == country)
        
    places = session.exec(statement).all()
    # Unique places, ideally we'd group by and count, but this is simple MVP
    popular_places = []
    seen = set()
    for p in places:
        if p.id not in seen:
            seen.add(p.id)
            popular_places.append(p)
            
    return popular_places[:10]

@router.post("/", response_model=Place)
def create_place(place_data: dict, session: Session = Depends(get_session)):
    external_id = place_data.get("external_id")
    if external_id:
        existing = session.exec(select(Place).where(Place.external_id == external_id)).first()
        if existing:
            return existing
            
    new_place = Place(**place_data)
    if not new_place.base_wait_time:
        new_place.base_wait_time = 15
        
    session.add(new_place)
    session.commit()
    session.refresh(new_place)
    return new_place

@router.get("/{place_id}", response_model=Place)
def get_place(place_id: int, session: Session = Depends(get_session)):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

@router.get("/{place_id}/prediction", response_model=Prediction)
def get_prediction(place_id: int, session: Session = Depends(get_session)):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
        
    prediction = compute_prediction_for_place(session, place)
    return prediction
