from datetime import datetime
from model.trip import Trip
import streamlit as st
from model.utils import execute_query, ModelConverter
from model.user_manager import UserManager


class TripManager:
    @staticmethod
    def get_recent_trips(limit=10):
        """Get the most recent trips from database"""
        query = """
            SELECT trips.*, username as creator_name 
            FROM trips 
            JOIN users ON trips.creator_id = users.user_id 
            ORDER BY trips.created_at DESC 
            LIMIT %s
        """
        trips_data = execute_query(query, (limit,))
        
        # Convert database records to Trip objects
        trips = []
        for data in trips_data:
            trip = ModelConverter.to_trip(data)
            trips.append(trip)
        
        return trips

    @staticmethod
    def get_trip_by_id(trip_id):
        """Get a trip by its ID from database"""
        query = """
            SELECT t.*, u.username as creator_name,
            GROUP_CONCAT(tp.user_id) as participants
            FROM trips t
            JOIN users u ON t.creator_id = u.user_id
            LEFT JOIN trip_participants tp ON t.trip_id = tp.trip_id
            WHERE t.trip_id = %s
            GROUP BY t.trip_id
        """
        trip_data = execute_query(query, (trip_id,))
        
        if not trip_data or len(trip_data) == 0:
            return None
            
        data = trip_data[0]  # Get first row since we're querying by primary key
        trip = ModelConverter.to_trip(data)
        
        # Add participants if any exist
        if data['participants']:
            for participant_id in data['participants'].split(','):
                # trip.add_participant(participant_id)
                p = UserManager.get_user_by_id(participant_id)
                trip.add_participant(p)

        items = TripManager.get_items_by_trip(trip_id)
        for item in items:
            trip.add_item(item) 
                
        return trip
    
    @staticmethod
    def get_items_by_trip(trip_id):
        """Get all items for a trip from database"""
        query = """
            SELECT * FROM items WHERE trip_id = %s
        """
        items_data = execute_query(query, (trip_id,))
        
        # Convert database records to Item objects
        items = []
        for data in items_data:
            print(data)
            item = ModelConverter.to_item(data)
            items.append(item)
            print(item.start_time)
        
        return items
    
    @staticmethod
    def get_creator(trip_id):
        """Get the creator of a trip"""
        query = """
            SELECT creator_id FROM trips WHERE trip_id = %s
        """
        creator_id = execute_query(query, (trip_id,))[0][0]
        return UserManager.get_user_by_id(creator_id)
    
    @staticmethod
    def create_trip(name, destination, start_date, end_date, creator_id):
        pass

    @staticmethod
    def delete_trip(trip_id):
        pass

    @staticmethod
    def update_trip(trip):
        pass    

