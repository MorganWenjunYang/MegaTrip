import streamlit as st
from trip import Trip

def show_home_page():
    st.success(f"Logged in as {st.session_state.username}")
    show_recent_trips()

def show_recent_trips():
    st.header("Recent Trips")
    
    if not st.session_state.trips:
        st.write("No trips found.")
        return
        
    sorted_trips = sorted(
        st.session_state.trips, 
        key=lambda x: x['created_at'], 
        reverse=True
    )
    
    for trip_data in sorted_trips[:10]:
        trip = Trip(
            trip_id=trip_data['trip_id'],
            name=trip_data['name'],
            destination=trip_data['destination'],
            start_date=trip_data['start_date'],
            end_date=trip_data['end_date'],
            creator_id=trip_data['creator_id']
        )
        for participant in trip_data['participants']:
            trip.add_participant(participant)
        trip.display_in_streamlit()