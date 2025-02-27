import streamlit as st
from controller.controller import handle_save_trip, handle_cancel_edit, handle_back_to_home

def show_sidebar():
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home", key="home", use_container_width=True):
            st.session_state.page = None
            st.rerun()
        if st.button("Profile", key="profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()


def show_trip_edit(trip):
    pass

def show_trip_details(trip):
    st.title(f"Trip Details: {trip.name}")
    st.write(f"🌍 Destination: {trip.destination}")
    st.write(f"📅 {trip.start_date} to {trip.end_date}")
    st.write(f"📌 Status: {trip.status}")
    if trip.note:
        st.write(f"📝 Note: {trip.note}")
    if trip.participants:
        st.write(f"👥 Participants: {', '.join(trip.participants)}")
    if trip.items:
        st.write("📋 Items:")
        for item in trip.items:
            st.write(f"- {item.name}")
    
    if st.button("Edit"):
        st.session_state.edit_mode = True
        st.rerun()
    
    if st.button("Back to Home"):
        handle_back_to_home()

def show_trip_short(trip):
        """Display trip details in Streamlit format"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(trip.name)
                st.write(f"🌍 Destination: {trip.destination}")
                st.write(f"📅 {trip.start_date} to {trip.end_date}")
                st.write(f"📌 Status: {trip.status}")  # display status
                if trip.note:
                    st.write(f"📝 Note: {trip.note}")  # display note if available
                if trip.participants:
                    st.write(f"👥 Participants: {', '.join(trip.participants)}")  # display user IDs
            with col2:
                if st.button("View Details", key=f"trip_{trip.trip_id}"):
                    st.session_state.current_trip_id = trip.trip_id
                    st.session_state.page = "trip_details"
                    st.rerun()