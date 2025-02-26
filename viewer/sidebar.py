import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home", key="home", use_container_width=True):
            st.session_state.page = None
            st.rerun()
        if st.button("Profile", key="profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()