import streamlit as st
from datetime import datetime, time
from model.trip import Trip
from model.item import Item
from model.trip_manager import TripManager
from model.utils import init_trip, init_item
from viewer.stutils import show_sidebar, edit_trip

def show_create_trip_page():
    show_sidebar()
    edit_trip(trip = None)

