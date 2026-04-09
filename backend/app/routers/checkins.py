from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Checkin, User, Place
from pydantic import BaseModel

router = APIRouter(prefix="/checkin", tags=["checkin"])

class CheckinRequest(BaseModel):
    place_id: int
    device_id: str

@router.post("/")
def create_checkin(request: CheckinRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.device_id == request.device_id)).first()
    if not user:
        user = User(device_id=request.device_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        
    place = session.get(Place, request.place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
        
    checkin = Checkin(place_id=place.id, user_id=user.id)
    session.add(checkin)
    session.commit()
    session.refresh(checkin)
    return {"status": "ok", "checkin_id": checkin.id}
