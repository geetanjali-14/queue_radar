import os
from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import Place
import random

MOCK_PLACES = [
    {"name": "Dermatology Clinic", "type": "clinic", "lat": 12.9716, "lng": 77.5946, "base_wait_time": 5},
    {"name": "Urban Salon", "type": "salon", "lat": 12.9720, "lng": 77.5950, "base_wait_time": 20},
    {"name": "PlayStation Cafe", "type": "cafe", "lat": 12.9730, "lng": 77.5960, "base_wait_time": 50},
    {"name": "City Hospital", "type": "hospital", "lat": 12.9750, "lng": 77.5980, "base_wait_time": 30},
    {"name": "Main Post Office", "type": "office", "lat": 12.9700, "lng": 77.5900, "base_wait_time": 15},
    {"name": "Greenwood Cafe", "type": "cafe", "lat": 12.9690, "lng": 77.5910, "base_wait_time": 10},
    {"name": "Hair & Care", "type": "salon", "lat": 12.9740, "lng": 77.5930, "base_wait_time": 25},
]

def seed_db():
    create_db_and_tables()
    with Session(engine) as session:
        for p_data in MOCK_PLACES:
            place = Place(**p_data)
            session.add(place)
        session.commit()
        print("Database seeded with mock places.")

if __name__ == "__main__":
    seed_db()
