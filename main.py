import streamlit as st
from pages import home, login, create_account, trip_details
from trip_manager import TripManager
from trip import Trip
from item import Item 
from user import User

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'current_trip_id' not in st.session_state:
    st.session_state.current_trip_id = None

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