import streamlit as st
from pages import home, login, create_account, trip_details
from trip_manager import TripManager
from trip import Trip
from item import Item 
from user import User

# Ensure the show_recent_trips function is defined before use
def show_recent_trips():
    st.header("Recent Trips")
    
    if not st.session_state.trips:
        st.write("No trips found.")
        return
        
    # Sort trips by created_at date in descending order
    sorted_trips = sorted(
        st.session_state.trips, 
        key=lambda x: x['created_at'], 
        reverse=True
    )
    
    # Convert dictionary data to Trip objects and display
    for trip_data in sorted_trips[:10]:
        trip = Trip(
            trip_id=trip_data['trip_id'],
            name=trip_data['name'],
            destination=trip_data['destination'],
            start_date=trip_data['start_date'],
            end_date=trip_data['end_date'],
            creator_id=trip_data['creator_id']
        )
        # Add participants if any
        for participant in trip_data['participants']:
            trip.add_participant(participant)
            
        # Use the standardized display method
        trip.display_in_streamlit()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "admin": "admin",
        "john": "john"
    }
if 'current_trip_id' not in st.session_state:
    st.session_state.current_trip_id = None

if 'trips' not in st.session_state:
    # Sample trip data
    st.session_state.trips = [
        {
            "trip_id": 1,
            "name": "Summer in Paris",
            "destination": "Paris, France",
            "start_date": "2025-06-01",
            "end_date": "2025-06-07",
            "creator_id": "admin",
            "participants": ["admin", "john"],  # list of user IDs
            "created_at": "2025-01-01",
            "status": "Active",  # new attribute for trip status
            "note": "Don't forget to visit the Eiffel Tower!"  # new attribute for trip note
        },
        {
            "trip_id": 2,
            "name": "Tokyo Adventure",
            "destination": "Tokyo, Japan",
            "start_date": "2025-07-15",
            "end_date": "2025-07-25",
            "creator_id": "admin",
            "participants": ["admin"],  # list of user IDs
            "created_at": "2025-01-15",
            "status": "Planned",  # new attribute for trip status
            "note": "Book tickets for the Ghibli Museum."  # new attribute for trip note
        },
        {
            "trip_id": 3,
            "name": "New York Weekend",
            "destination": "New York, USA",
            "start_date": "2025-03-01",
            "end_date": "2025-03-03",
            "creator_id": "john",
            "participants": ["john", "admin"],  # list of user IDs
            "created_at": "2025-02-01",
            "status": "Completed",  # new attribute for trip status
            "note": "Had a great time at Central Park."  # new attribute for trip note
        }
    ]

st.logo(
    "./assets/logo.jpg",
    icon_image="./assets/logo.jpg",
)

# Page routing
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login.show_login_page()
    elif st.session_state.page == "create_account":
        create_account.show_create_account_page()
else:
    if st.session_state.page == "trip_details":
        trip_details.show_trip_details_page()
    else:
        home.show_home_page()