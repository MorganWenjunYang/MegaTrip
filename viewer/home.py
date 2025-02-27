import streamlit as st
from model.trip import Trip
from trip_manager import TripManager
from viewer.stutils import show_sidebar, show_trip_short

def show_home_page():
    st.success(f"Logged in as {st.session_state.username}")
    show_sidebar()
    
    if st.button("New Trip +", key="new_trip", help="Create a new trip"):
        st.session_state.page = "create_trip"
        st.rerun()
    
    show_recent_trips()

def show_recent_trips():
    st.header("Recent Trips")
    
    recent_trips = TripManager.get_recent_trips()  # Fetch recent trips from trip_manager
    
    if not recent_trips:
        st.write("No trips found.")
        return
        
    for trip in recent_trips[:10]:
        show_trip_short(trip)