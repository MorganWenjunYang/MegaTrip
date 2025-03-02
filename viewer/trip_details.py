import streamlit as st
from model.trip import Trip
from model.trip_manager import TripManager
from controller.controller import handle_save_trip, handle_cancel_edit, handle_back_to_home
from viewer.stutils import show_sidebar, show_trip_details, edit_trip

def show_trip_details_page():
    show_sidebar()
    if st.session_state.current_trip_id:
        trip = TripManager.get_trip_by_id(st.session_state.current_trip_id)
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