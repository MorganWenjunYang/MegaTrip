from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from typing import Optional, List
from decimal import Decimal

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserWithTrips(User):
    created_trips: List['Trip'] = []
    participated_trips: List['Trip'] = []

# Item schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: Optional[date] = None
    location: Optional[str] = None
    note: Optional[str] = None
    charge: Optional[Decimal] = Decimal('0.00')
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    payer: Optional[str] = None

class ItemCreate(ItemBase):
    trip_id: int

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int
    trip_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Trip schemas
class TripBase(BaseModel):
    name: str
    destination: str
    start_date: date
    end_date: date
    status: Optional[str] = 'Planned'
    note: Optional[str] = None

class TripCreate(TripBase):
    creator_id: int

class TripUpdate(TripBase):
    pass

class Trip(TripBase):
    trip_id: int
    creator_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TripWithDetails(Trip):
    creator: User
    participants: List[User] = []
    items: List[Item] = []

# Response schemas
class LoginResponse(BaseModel):
    user: User
    message: str

class MessageResponse(BaseModel):
    message: str 