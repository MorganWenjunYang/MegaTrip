import streamlit as st
from utils import execute_query

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
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        user = execute_query(query, (username, password))
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]['user_id']
            st.success("Logged in as {}".format(username))
            st.rerun()
        else:
            st.error("Invalid username or password")

    if create_new_button:
        st.session_state.page = "create_account"
        st.rerun()