from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MegaTrip API",
    description="API for MegaTrip application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# User endpoints
@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/users/login", response_model=schemas.LoginResponse)
def login_user(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_credentials(db, username=user_login.username, password=user_login.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user": db_user, "message": "Login successful"}

@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/api/users/{user_id}", response_model=schemas.MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Trip endpoints
@app.post("/api/trips/", response_model=schemas.Trip)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    # Verify creator exists
    db_user = crud.get_user(db, user_id=trip.creator_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Creator not found")
    return crud.create_trip(db=db, trip=trip)

@app.get("/api/trips/{trip_id}", response_model=schemas.TripWithDetails)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@app.put("/api/trips/{trip_id}", response_model=schemas.Trip)
def update_trip(trip_id: int, trip_update: schemas.TripUpdate, db: Session = Depends(get_db)):
    db_trip = crud.update_trip(db, trip_id=trip_id, trip_update=trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@app.delete("/api/trips/{trip_id}", response_model=schemas.MessageResponse)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    success = crud.delete_trip(db, trip_id=trip_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip deleted successfully"}

@app.get("/api/trips/", response_model=List[schemas.Trip])
def get_recent_trips(limit: int = 10, db: Session = Depends(get_db)):
    trips = crud.get_recent_trips(db, limit=limit)
    return trips

@app.get("/api/users/{user_id}/created-trips", response_model=List[schemas.Trip])
def get_user_created_trips(user_id: int, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_trips_by_creator(db, creator_id=user_id)

@app.get("/api/users/{user_id}/participated-trips", response_model=List[schemas.Trip])
def get_user_participated_trips(user_id: int, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_trips_by_participant(db, user_id=user_id)

@app.post("/api/trips/{trip_id}/participants/{user_id}", response_model=schemas.MessageResponse)
def add_trip_participant(trip_id: int, user_id: int, db: Session = Depends(get_db)):
    success = crud.add_trip_participant(db, trip_id=trip_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not add participant")
    return {"message": "Participant added successfully"}

@app.delete("/api/trips/{trip_id}/participants/{user_id}", response_model=schemas.MessageResponse)
def remove_trip_participant(trip_id: int, user_id: int, db: Session = Depends(get_db)):
    success = crud.remove_trip_participant(db, trip_id=trip_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not remove participant")
    return {"message": "Participant removed successfully"}

# Item endpoints
@app.post("/api/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    # Verify trip exists
    db_trip = crud.get_trip(db, trip_id=item.trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return crud.create_item(db=db, item=item)

@app.get("/api/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/api/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/api/items/{item_id}", response_model=schemas.MessageResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

@app.get("/api/trips/{trip_id}/items", response_model=List[schemas.Item])
def get_trip_items(trip_id: int, db: Session = Depends(get_db)):
    # Verify trip exists
    db_trip = crud.get_trip(db, trip_id=trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return crud.get_items_by_trip(db, trip_id=trip_id) 