import streamlit as st
from model.trip_manager import TripManager
from model.user_manager import UserManager
from model.utils import execute_query
from viewer.home import show_sidebar  # Import the show_sidebar function

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
        
    for trip in trips:
        with st.expander(f"🎯 {trip['name']} ({trip['destination']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dates:** {trip['start_date']} - {trip['end_date']}")
                st.write(f"**Status:** {trip['status']}")
            with col2:
                # st.write(f"**Participants:** {trip['participant_count']}")
                if trip['note']:
                    st.write(f"**Note:** {trip['note']}")
            
            if st.button("View Details", key=f"view_{trip['trip_id']}"):
                st.session_state.current_trip_id = trip['trip_id']
                st.session_state.page = "trip_details"
                st.rerun()

def show_participated_trips():
    st.subheader("Trips You're Participating In")

    trips = UserManager.get_participated_trips(st.session_state.user_id)  # Use the get_participated_trips method from UserManager
    
    if not trips:
        st.write("You're not participating in any trips created by others.")
        return
        
    for trip in trips:
        with st.expander(f"✈️ {trip['name']} ({trip['destination']})"):
            col1, col2 = st.columns(2)
            with col1:
                # st.write(f"**Created by:** {trip['creator_name']}")
                st.write(f"**Dates:** {trip['start_date']} - {trip['end_date']}")
            with col2:
                st.write(f"**Status:** {trip['status']}")
                if trip['note']:
                    st.write(f"**Note:** {trip['note']}")
            
            if st.button("View Details", key=f"view_part_{trip['trip_id']}"):
                st.session_state.current_trip_id = trip['trip_id']
                st.session_state.page = "trip_details"
                st.rerun()