import mysql.connector
from config import DB_CONFIG
from datetime import datetime
from typing import List, Dict, Any
from model.user import User
from model.trip import Trip
from model.item import Item
from datetime import datetime, time

def connect_to_db():
    """Create and return a database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None, fetch=True):
    """Execute a query and optionally return results"""
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

class ModelConverter:
    @staticmethod
    def to_user(db_record: Dict[str, Any]) -> User:
        """Convert database record to User object"""
        if not db_record:
            return None
            
        return User(
            user_id=db_record['user_id'],
            username=db_record['username']
        )

    @staticmethod
    def to_trip(db_record: Dict[str, Any], items: List[Item] = None, 
                participants: List[str] = None) -> Trip:
        """Convert database record to Trip object"""
        if not db_record:
            return None
            
        return Trip(
            trip_id=db_record['trip_id'],
            name=db_record['name'],
            destination=db_record['destination'],
            start_date=db_record['start_date'],
            end_date=db_record['end_date'],
            creator_id=db_record['creator_id'],
            created_at=db_record['created_at'],
            status=db_record['status'],
            note=db_record['note'],
            # items=items or [],
            # participants=participants or [],
            # created_at=db_record.get('created_at')
        )

    @staticmethod
    def to_item(db_record: Dict[str, Any]) -> Item:
        """Convert database record to Item object"""
        if not db_record:
            return None
            
        return Item(
            item_id=db_record['item_id'],
            trip_id=db_record['trip_id'],
            name=db_record['name'],
            description=db_record['description'],
            date=db_record['date'],
            start_time=db_record['start_time'],
            end_time=db_record['end_time'],
            location=db_record.get('location'),
            note=db_record.get('note'),
            charge=db_record.get('charge', 0.0),
            payer=db_record.get('payer'),
            split=db_record.get('split', {})
        )
    
def init_item():
    """Initialize an empty item with default values"""
    return {
        "name": "",
        "description": "",
        "date": datetime.today().date(),
        "start_time": time(9, 0),  # Default 9:00 AM
        "end_time": time(10, 0),   # Default 10:00 AM
        "location": "",
        "note": "",
        "charge": 0.0,
        "payer": "",
        "split": {}
    }

def init_trip():
    """Initialize an empty item with default values"""
    return {
        "name": "",
        "destination": "",
        "start_date": datetime.today().date(),
        "end_date": datetime.today().date(),
        "status": "Active",
        "note": "",
        "items": []
    }