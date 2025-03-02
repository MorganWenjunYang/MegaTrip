import streamlit as st
from model.trip_manager import TripManager
from model.user_manager import UserManager
from model.utils import execute_query
from viewer.home import show_sidebar
from viewer.stutils import show_trip_expander

def show_profile_page():
    if not st.session_state.logged_in:
        st.warning("Please log in to view your profile")
        return

    st.title(f"Profile - {st.session_state.username}")
    show_sidebar()
    
    # Create tabs for different trip categories
    created_tab, participated_tab = st.tabs(["Created Trips", "Participated Trips"])
    
    with created_tab:
        show_created_trips()
    
    with participated_tab:
        show_participated_trips()

def show_created_trips():
    st.subheader("Trips You Created")

    trips = UserManager.get_created_trips(st.session_state.user_id)  # Use the get_created_trips method from UserManager
    if not trips:
        st.write("You haven't created any trips yet.")
        return
    
    show_trip_expander(trips, context="created")  # Add context parameter

def show_participated_trips():
    st.subheader("Trips You're Participating In")

    trips = UserManager.get_participated_trips(st.session_state.user_id)  # Use the get_participated_trips method from UserManager
    
    if not trips:
        st.write("You're not participating in any trips created by others.")
        return
        
    show_trip_expander(trips, context="participated")  # Add context parameter