import streamlit as st
from api_client import api_client
from viewer.stutils import show_sidebar, show_trip_details, edit_trip, handle_back_to_home

def show_trip_details_page():
    show_sidebar()
    if st.session_state.current_trip_id:
        trip = api_client.get_trip(st.session_state.current_trip_id)  # Use API client instead of TripManager
        if trip:
            if 'edit_mode' not in st.session_state:
                st.session_state.edit_mode = False

            if st.session_state.edit_mode:
                edit_trip(trip)
            else:
                show_trip_details(trip)
        else:
            st.error("Trip not found")
            handle_back_to_home()
    else:
        st.error("No trip selected")
        handle_back_to_home()