import mysql.connector
from datetime import datetime
from trip import Trip
import streamlit as st

class TripManager:
    @staticmethod
    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="megatrip"
        )

    @staticmethod
    def get_recent_trips(limit=10):
        """Get the most recent trips from database"""
        try:
            db = TripManager.connect_db()
            cursor = db.cursor(dictionary=True)
            
            query = """
                SELECT trips.*, users.name as creator_name 
                FROM trips 
                JOIN users ON trips.creator_id = users.user_id 
                ORDER BY trips.created_at DESC 
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            trips_data = cursor.fetchall()
            
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
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
            
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()

    @staticmethod
    def get_trip_by_id(trip_id):
        """Get a trip by its ID from in-memory data"""
        for trip_data in st.session_state.trips:
            if trip_data['trip_id'] == trip_id:
                trip = Trip(
                    trip_id=trip_data['trip_id'],
                    name=trip_data['name'],
                    destination=trip_data['destination'],
                    start_date=trip_data['start_date'],
                    end_date=trip_data['end_date'],
                    creator_id=trip_data['creator_id']
                )
                trip.status = trip_data['status']
                trip.note = trip_data['note']
                for participant in trip_data['participants']:
                    trip.add_participant(participant)
                return trip
        return None

    @staticmethod
    def update_trip(updated_trip):
        for trip_data in st.session_state.trips:
            if trip_data['trip_id'] == updated_trip.trip_id:
                trip_data['name'] = updated_trip.name
                trip_data['destination'] = updated_trip.destination
                trip_data['start_date'] = updated_trip.start_date
                trip_data['end_date'] = updated_trip.end_date
                trip_data['status'] = updated_trip.status
                trip_data['note'] = updated_trip.note
                break
