import streamlit as st
from trip_manager import TripManager
from trip import Trip
from item import Item 
from user import User
from viewer import create_account, login, profile, trip_details, home, profile

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'current_trip_id' not in st.session_state:
    st.session_state.current_trip_id = None
if 'username' not in st.session_state: 
    st.session_state.username = None
if 'user_id' not in st.session_state: 
    st.session_state.user_id = None

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
    elif st.session_state.page == "profile":
        profile.show_profile_page()   
    else:
        home.show_home_page()