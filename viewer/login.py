import streamlit as st
from api_client import api_client

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
        if username and password:
            login_result = api_client.login(username, password)
            if login_result:
                user = login_result["user"]
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_id = user["user_id"]
                st.success("Logged in as {}".format(username))
                st.rerun()
            # Error handling is done in api_client._handle_response
        else:
            st.error("Please enter both username and password")

    if create_new_button:
        st.session_state.page = "create_account"
        st.rerun()