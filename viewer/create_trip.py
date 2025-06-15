import streamlit as st
from viewer.stutils import show_sidebar, edit_trip

def show_create_trip_page():
    show_sidebar()
    edit_trip(trip = None)

