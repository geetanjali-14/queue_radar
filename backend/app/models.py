from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    checkins: List["Checkin"] = Relationship(back_populates="user")

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str] = Field(default=None, index=True)
    name: str
    city: Optional[str] = Field(default=None, index=True)
    country: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    lat: float
    lng: float
    base_wait_time: int = Field(default=15)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    checkins: List["Checkin"] = Relationship(back_populates="place")
    predictions: List["Prediction"] = Relationship(back_populates="place")
    crowd_logs: List["CrowdLog"] = Relationship(back_populates="place")

class Checkin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    place_id: int = Field(foreign_key="place.id")
    user_id: int = Field(foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    place: Place = Relationship(back_populates="checkins")
    user: User = Relationship(back_populates="checkins")

class CrowdLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    place_id: int = Field(foreign_key="place.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    crowd_level: str
    wait_time_predicted: int
    
    place: Place = Relationship(back_populates="crowd_logs")

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    place_id: int = Field(foreign_key="place.id", unique=True)
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    wait_time_min: int
    crowd_level: str
    best_time: str
    trending: str = Field(default="steady") # increasing, decreasing, steady
    
    place: Place = Relationship(back_populates="predictions")
