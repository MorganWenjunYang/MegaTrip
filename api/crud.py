from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from . import models, schemas
from typing import List, Optional

# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_credentials(db: Session, username: str, password: str) -> Optional[models.User]:
    return db.query(models.User).filter(
        and_(models.User.username == username, models.User.password == password)
    ).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Trip CRUD operations
def get_trip(db: Session, trip_id: int) -> Optional[models.Trip]:
    return db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()

def get_trips_by_creator(db: Session, creator_id: int) -> List[models.Trip]:
    return db.query(models.Trip).filter(models.Trip.creator_id == creator_id).all()

def get_trips_by_participant(db: Session, user_id: int) -> List[models.Trip]:
    return db.query(models.Trip).join(models.trip_participants).filter(
        models.trip_participants.c.user_id == user_id
    ).all()

def get_recent_trips(db: Session, limit: int = 10) -> List[models.Trip]:
    return db.query(models.Trip).order_by(models.Trip.created_at.desc()).limit(limit).all()

def create_trip(db: Session, trip: schemas.TripCreate) -> models.Trip:
    db_trip = models.Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

def update_trip(db: Session, trip_id: int, trip_update: schemas.TripUpdate) -> Optional[models.Trip]:
    db_trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    if db_trip:
        update_data = trip_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_trip, field, value)
        db.commit()
        db.refresh(db_trip)
        return db_trip
    return None

def delete_trip(db: Session, trip_id: int) -> bool:
    db_trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    if db_trip:
        db.delete(db_trip)
        db.commit()
        return True
    return False

def add_trip_participant(db: Session, trip_id: int, user_id: int) -> bool:
    db_trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if db_trip and db_user and db_user not in db_trip.participants:
        db_trip.participants.append(db_user)
        db.commit()
        return True
    return False

def remove_trip_participant(db: Session, trip_id: int, user_id: int) -> bool:
    db_trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if db_trip and db_user and db_user in db_trip.participants:
        db_trip.participants.remove(db_user)
        db.commit()
        return True
    return False

# Item CRUD operations
def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.item_id == item_id).first()

def get_items_by_trip(db: Session, trip_id: int) -> List[models.Item]:
    return db.query(models.Item).filter(models.Item.trip_id == trip_id).all()

def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate) -> Optional[models.Item]:
    db_item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False 