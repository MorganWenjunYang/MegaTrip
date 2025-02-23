import streamlit as st

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