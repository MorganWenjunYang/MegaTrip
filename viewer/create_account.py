import streamlit as st
from utils import execute_query

def show_create_account_page():
    # Title and welcome message
    st.title("Welcome to MegaTrip!")
    st.write("We are excited to have you here. Explore and enjoy your trip planning experience!")
    st.write("Don't use your real password. Inner use only.")
    form_container = st.sidebar.empty()
    with form_container:
        st.sidebar.title("Create New Account")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        create_account_button = st.sidebar.button("Create Account", use_container_width=True)
        back_to_login_button = st.sidebar.button("Back to Login", use_container_width=True)

    if create_account_button:
        if new_username and new_password:
            query = "SELECT * FROM users WHERE username = %s"
            user = execute_query(query, (new_username,))
            if user:
                st.error("Username already exists")
            else:
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                execute_query(query, (new_username, new_password), fetch=False)
                st.success("Account created for {}".format(new_username))
                st.session_state.page = "login"
                st.rerun()
        else:
            st.error("Please enter a valid username and password")

    if back_to_login_button:
        st.session_state.page = "login"
        st.rerun()