from sqlmodel import Session, select
from datetime import datetime, timedelta
from app.models import Place, Checkin, Prediction, CrowdLog
from typing import Optional

HIGH_THRESHOLD = 5
MEDIUM_THRESHOLD = 2

def compute_prediction_for_place(session: Session, place: Place) -> Prediction:
    now = datetime.utcnow()
    thirty_mins_ago = now - timedelta(minutes=30)
    
    # Get recent checkins
    statement = select(Checkin).where(Checkin.place_id == place.id).where(Checkin.timestamp >= thirty_mins_ago)
    recent_checkins = session.exec(statement).all()
    count = len(recent_checkins)
    
    crowd_level = "LOW"
    wait_time_added = 0
    trending = "steady"
    
    if count == 0:
        # Check total historical checkins to see if it's completely new or just empty right now
        total_statement = select(Checkin).where(Checkin.place_id == place.id).limit(1)
        any_history = session.exec(total_statement).first()
        if not any_history:
            crowd_level = "Not enough data yet"
            
    if count >= HIGH_THRESHOLD:
        crowd_level = "HIGH"
        wait_time_added = 30
    elif count >= MEDIUM_THRESHOLD:
        crowd_level = "MEDIUM"
        wait_time_added = 15
        
    total_wait = place.base_wait_time + wait_time_added
    
    # Calculate previous 30 min count for trending
    sixty_mins_ago = now - timedelta(minutes=60)
    prev_statement = select(Checkin).where(Checkin.place_id == place.id).where(Checkin.timestamp >= sixty_mins_ago).where(Checkin.timestamp < thirty_mins_ago)
    prev_checkins = session.exec(prev_statement).all()
    prev_count = len(prev_checkins)
    
    if count > prev_count:
        trending = "increasing"
    elif count < prev_count:
        trending = "decreasing"
        
    # Best time heuristic: Usually 2 hours from now if HIGH
    best_time = (now + timedelta(hours=2)).strftime("%I:%M %p") if crowd_level == "HIGH" else "Now"
    
    # Upsert Prediction
    pred_statement = select(Prediction).where(Prediction.place_id == place.id)
    prediction = session.exec(pred_statement).first()
    if not prediction:
        prediction = Prediction(place_id=place.id)
        
    prediction.wait_time_min = total_wait
    prediction.crowd_level = crowd_level
    prediction.best_time = best_time
    prediction.trending = trending
    prediction.computed_at = now
    
    session.add(prediction)
    
    # Log the crowd
    log = CrowdLog(place_id=place.id, timestamp=now, crowd_level=crowd_level, wait_time_predicted=total_wait)
    session.add(log)
    
    session.commit()
    session.refresh(prediction)
    
    return prediction
