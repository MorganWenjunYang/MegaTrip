import streamlit as st
from trip_manager import TripManager
from utils import execute_query
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
    query = """
        SELECT t.*
        FROM trips t 
                WHERE t.creator_id = %s 
                ORDER BY t.created_at DESC
    """
    trips = execute_query(query, (st.session_state.user_id,))  # Use user_id instead of username
    
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
    query = """
        SELECT t.* 
        FROM trips t 
        JOIN trip_participants tp ON t.trip_id = tp.trip_id 
                WHERE tp.user_id = %s 
        ORDER BY t.created_at DESC
    """
    trips = execute_query(query, (st.session_state.user_id,))
    
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