import streamlit as st
from api_client import api_client
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
    
    recent_trips = api_client.get_recent_trips()  # Use API client instead of TripManager
    
    if not recent_trips:
        st.write("No trips found.")
        return
        
    for trip in recent_trips[:10]:
        show_trip_short(trip)