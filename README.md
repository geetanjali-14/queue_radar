# Queue Radar MVP

Queue Radar is a decision engine that helps users decide WHEN to visit a place by predicting wait times and crowd levels.

## System Architecture

The MVP is built with a lightweight but scalable stack:
- **Backend:** FastAPI (Python) for rapid, high-performance API development.
- **Database:** SQLite (for MVP simplicity, easily swappable with PostgreSQL via SQLModel).
- **ORM:** SQLModel (combines Pydantic and SQLAlchemy).
- **Frontend:** Next.js (App Router) + Tailwind CSS.

## Database Schema (SQLModel)

1. **User:** Tracks unique devices/users (`id`, `device_id`, `created_at`).
2. **Place:** Stores business locations (`id`, `name`, `type`, `lat`, `lng`, `base_wait_time`).
3. **Checkin:** Fact table for user check-ins (`id`, `place_id`, `user_id`, `timestamp`).
4. **CrowdLog:** Time-series records of crowd levels (`id`, `place_id`, `timestamp`, `crowd_level`, `wait_time_predicted`).
5. **Prediction:** Cached table for the latest predicted wait times and best times to visit.

## Prediction Engine Logic

The core logic handles moving queues and predicting trends:
- It fetches check-ins from the last 30 minutes.
- Uses thresholds (`>= 5` for HIGH, `>= 2` for MEDIUM, otherwise LOW).
- Computes trend (`increasing`, `decreasing`, `steady`) by comparing the past 30 mins with the 30 mins before that.
- Calculates an estimated wait time by adding a delay factor to the intrinsic `base_wait_time` of the location.
- Predicts the **Best Time to Visit** based on historical drop-offs or standard business logic (e.g., 2 hours later if currently HIGH).

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### 1. Backend Setup
Navigate to the root directory where the `backend` folder is located:
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Seed the mock database (10 places)
PYTHONPATH=backend python backend/seed.py

# Start the FastAPI server
PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
Open a new terminal session and navigate to the `frontend` directory:
```bash
cd frontend

# Install dependencies
npm install

# Start the Next.js development server
npm run dev
```

### 3. Usage
- Go to `http://localhost:3000` to view the **Queue Radar Dashboard**.
- Click on any mocked location (e.g., Urban Salon, City Hospital).
- Click the **"Check In Now"** button multiple times (simulating different users) to see the Crowd Level turn from Green (LOW) to Yellow (MEDIUM) and eventually Red (HIGH), dynamically updating the wait time and recommendations!

## Future Improvements for V2
- Shift from SQLite to PostgreSQL + Redis Cache.
- Implement Celery jobs for background time-series aggregation.
- Deploy a real Machine Learning pipeline (e.g., Scikit-learn Random Forest) based on historical `CrowdLog` data matrices.
