from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, Decimal, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for many-to-many relationship between trips and users (participants)
trip_participants = Table(
    'trip_participants',
    Base.metadata,
    Column('trip_id', Integer, ForeignKey('trips.trip_id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # Relationships
    created_trips = relationship("Trip", back_populates="creator", foreign_keys="Trip.creator_id")
    participated_trips = relationship("Trip", secondary=trip_participants, back_populates="participants")

class Trip(Base):
    __tablename__ = "trips"
    
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=func.current_timestamp())
    status = Column(Enum('Active', 'Planned', 'Completed', name='trip_status'), default='Planned')
    note = Column(Text)
    
    # Relationships
    creator = relationship("User", back_populates="created_trips", foreign_keys=[creator_id])
    participants = relationship("User", secondary=trip_participants, back_populates="participated_trips")
    items = relationship("Item", back_populates="trip", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    date = Column(Date)
    location = Column(String(255))
    note = Column(Text)
    charge = Column(Decimal(10, 2), default=0.00)
    start_time = Column(Time)
    end_time = Column(Time)
    payer = Column(String(50))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    trip = relationship("Trip", back_populates="items") 