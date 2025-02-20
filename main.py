import streamlit as st
from trip import Trip
from item import Item 
from user import User

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "admin": "admin"
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
            "participants": ["admin", "john"],
            "created_at": "2025-01-01"
        },
        {
            "trip_id": 2,
            "name": "Tokyo Adventure",
            "destination": "Tokyo, Japan",
            "start_date": "2025-07-15",
            "end_date": "2025-07-25",
            "creator_id": "admin",
            "participants": ["admin"],
            "created_at": "2025-01-15"
        },
        {
            "trip_id": 3,
            "name": "New York Weekend",
            "destination": "New York, USA",
            "start_date": "2025-03-01",
            "end_date": "2025-03-03",
            "creator_id": "john",
            "participants": ["john", "admin"],
            "created_at": "2025-02-01"
        }
    ]
# Custom CSS to position the logo
st.markdown("""
    <style>
        .logo-container {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            padding: 10px;
        }
        .logo-img {
            width: 100px;  /* Adjust size as needed */
        }
    </style>
    """, unsafe_allow_html=True)

# Logo in top-left corner
st.markdown("""
    <div class="logo-container">
        <img class="logo-img" src="assets/logo.png">
    </div>
    """, unsafe_allow_html=True)

# Main content with some spacing to avoid overlap with logo
st.markdown("<br><br>", unsafe_allow_html=True) 

# Title and welcome message
st.title("Welcome to MegaTrip!")
st.write("We are excited to have you here. Explore and enjoy your trip planning experience!")

# Create a container for the login and registration forms
form_container = st.sidebar.empty()

if not st.session_state.logged_in:
    if st.session_state.page == "login":
        with form_container:
            st.sidebar.title("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            login_button = st.sidebar.button("Login")
            create_new_button = st.sidebar.button("New User?")

        if login_button:
            if username in st.session_state.user_data and st.session_state.user_data[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in as {}".format(username))
            else:
                st.error("Invalid username or password")

        if create_new_button:
            st.session_state.page = "create_account"

    elif st.session_state.page == "create_account":
        with form_container:
            st.sidebar.title("Create New Account")
            new_username = st.sidebar.text_input("New Username")
            new_password = st.sidebar.text_input("New Password", type="password")
            create_account_button = st.sidebar.button("Create Account")
            back_to_login_button = st.sidebar.button("Back to Login")

        if create_account_button:
            if new_username and new_password:
                if new_username in st.session_state.user_data:
                    st.error("Username already exists")
                else:
                    st.session_state.user_data[new_username] = new_password
                    st.success("Account created for {}".format(new_username))
                    st.session_state.page = "login"
            else:
                st.error("Please enter a valid username and password")

        if back_to_login_button:
            st.session_state.page = "login"
else:
    if st.session_state.page == "trip_details":
        # Show trip details page
        if st.session_state.current_trip_id:
            trip = TripManager.get_trip_by_id(st.session_state.current_trip_id)
            if trip:
                st.title(f"Trip Details: {trip.name}")
                # Add your trip details display logic here
                if st.button("Back to Home"):
                    st.session_state.page = "home"
                    st.session_state.current_trip_id = None
        else:
            st.error("No trip selected")
            st.session_state.page = "home"
    else:
        # Show home page with recent trips
        st.success(f"Logged in as {st.session_state.username}")
        show_recent_trips()

# def show_recent_trips():
#     st.header("Recent Trips")
#     recent_trips = TripManager.get_recent_trips()
    
#     if not recent_trips:
#         st.write("No trips found.")
#         return
        
#     for trip in recent_trips:
#         trip.display_in_streamlit()

# Modify the show_recent_trips function to use in-memory data

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