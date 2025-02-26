from datetime import datetime
from trip import Trip
import streamlit as st
from utils import execute_query

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
            trip = Trip(
                data['trip_id'],
                data['name'],
                data['destination'],
                data['start_date'],
                data['end_date'],
                data['creator_id']
            )
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
        trip = Trip(
            trip_id=data['trip_id'],
            name=data['name'],
            destination=data['destination'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            creator_id=data['creator_id']
        )
        trip.status = data['status']
        trip.note = data['note']
        
        # Add participants if any exist
        if data['participants']:
            for participant_id in data['participants'].split(','):
                trip.add_participant(participant_id)
                
        return trip
    
    @staticmethod
    def create_trip(name, destination, start_date, end_date, creator_id):
        pass

    @staticmethod
    def delete_trip(trip_id):
        pass

    @staticmethod
    def update_trip(trip):
        pass    

