import streamlit as st
from model.utils import execute_query
from model.user_manager import UserManager

def show_login_page():
    form_container = st.sidebar.empty()
    # Title and welcome message
    st.title("Welcome to MegaTrip!")
    st.write("We are excited to have you here. Explore and enjoy your trip planning experience!")
    st.write("Don't use your real password. Inner use only.")
    with form_container:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.button("Login", use_container_width=True)
        create_new_button = st.sidebar.button("New User?", use_container_width=True)

    if login_button:
        user = UserManager.get_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user['user_id']
            st.success("Logged in as {}".format(username))
            st.rerun()
        else:
            st.error("Invalid username or password")

    if create_new_button:
        st.session_state.page = "create_account"
        st.rerun()