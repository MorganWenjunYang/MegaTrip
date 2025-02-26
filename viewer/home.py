import streamlit as st
from trip import Trip
from trip_manager import TripManager
from viewer.sidebar import show_sidebar 

def show_home_page():
    st.success(f"Logged in as {st.session_state.username}")
    show_sidebar()
    show_recent_trips()

def show_recent_trips():
    st.header("Recent Trips")
    
    recent_trips = TripManager.get_recent_trips()  # Fetch recent trips from trip_manager
    
    if not recent_trips:
        st.write("No trips found.")
        return
        
    for trip in recent_trips[:10]:
        trip.display_in_streamlit()