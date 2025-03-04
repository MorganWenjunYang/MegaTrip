import streamlit as st
from model.trip_manager import TripManager

def handle_cancel_edit():
    st.session_state.edit_mode = False
    del st.session_state.staged_trip
    st.rerun()

def handle_back_to_home():
    st.session_state.page = "home"
    st.session_state.current_trip_id = None
    del st.session_state.staged_trip
    st.rerun()

def handle_input_check(staged):
    if not staged:
        st.warning("Please fill in all required fields")
        return

    if not staged['start_date'] or not staged['end_date']:
        st.warning("Please select a start and end date")
        return

    if staged['start_date'] > staged['end_date']:
        st.warning("End date must be after start date")
        return

    if not staged['destination']:
        st.warning("Please enter a destination")
        return

    if not staged['status']:
        st.warning("Please enter a status")
        return

    return True

def handle_save_trip(staged):

    if not handle_input_check(staged):
        return

    TripManager.create_trip(staged)

    st.session_state.edit_mode = False
    del st.session_state.staged_trip
    st.session_state.page = "home"
    st.session_state.current_trip_id = None
    st.rerun()

def handle_update_trip(staged):

    if not handle_input_check(staged):
        return

    TripManager.update_trip(staged)
    st.session_state.edit_mode = False
    del st.session_state.staged_trip
    st.session_state.page = "home"
    st.session_state.current_trip_id = None
    st.rerun()

def handle_save_item():
    pass

def handle_add_participant():
    pass

def handle_remove_participant():
    pass

