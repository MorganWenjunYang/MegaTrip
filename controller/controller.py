import streamlit as st
from model.trip_manager import TripManager

def handle_view_details(trip_id):
    st.session_state.current_trip_id = trip_id
    st.session_state.page = "trip_details"

def handle_edit_trip(trip_id):
    st.session_state.current_trip_id = trip_id
    st.session_state.page = "trip_details"
    st.session_state.edit_mode = True

def handle_save_trip(trip, new_name, new_destination, new_start_date, new_end_date, new_status, new_note):
    trip.name = new_name
    trip.destination = new_destination
    trip.start_date = new_start_date
    trip.end_date = new_end_date
    trip.status = new_status
    trip.note = new_note
    # Items are already updated in the trip object
    TripManager.update_trip(trip)
    st.session_state.edit_mode = False
    st.success("Trip details updated successfully")

def handle_cancel_edit():
    st.session_state.edit_mode = False

def handle_back_to_home():
    st.session_state.page = "home"
    st.session_state.current_trip_id = None

# def handle_create_trip(name, destination, start_date, end_date, status, note):
#     new_trip = Trip(
#         name=name,
#         destination=destination,
#         start_date=start_date,
#         end_date=end_date,
#         status=status,
#         note=note,
#         owner=st.session_state.username
#     )
#     TripManager.create_trip(new_trip)
#     st.session_state.page = None
#     st.success("Trip created successfully!")