import streamlit as st
from datetime import datetime
from trip import Trip
from trip_manager import TripManager
from viewer.stutils import show_sidebar

def show_create_trip_page():
    show_sidebar()
    st.header("Create New Trip")
    
    # Initialize items list in session state if not exists
    if 'trip_items' not in st.session_state:
        st.session_state.trip_items = []
    
    with st.form("new_trip_form"):
        name = st.text_input("Trip Name", key="trip_name")
        destination = st.text_input("Destination", key="destination")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", key="start_date")
        with col2:
            end_date = st.date_input("End Date", key="end_date")
        
        status = st.selectbox(
            "Status",
            options=["Planning", "Ongoing", "Completed", "Cancelled"],
            key="status"
        )
        
        note = st.text_area("Notes", key="note")
        
        # Add items section
        st.subheader("Items")
        for idx, item in enumerate(st.session_state.trip_items):
            st.text(f"• {item}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_item = st.text_input("Add an item", key="new_item")
        with col2:
            add_item = st.form_submit_button("+ Add", type="secondary")
            if add_item and new_item:
                st.session_state.trip_items.append(new_item)
                st.rerun()
        
        submit = st.form_submit_button("Create Trip")
        
        if submit:
            if not name or not destination:
                st.error("Trip name and destination are required!")
                return
                
            if end_date < start_date:
                st.error("End date cannot be earlier than start date!")
                return
                
            new_trip = Trip(
                name=name,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                status=status,
                note=note,
                owner=st.session_state.username,
                items=st.session_state.trip_items  # Include items in trip creation
            )
            
            TripManager.create_trip(new_trip)
            st.session_state.trip_items = []  # Clear items after creation
            st.success("Trip created successfully!")
            st.session_state.page = None  # Return to home page
            st.rerun()
    
    if st.button("Cancel"):
        st.session_state.page = None
        st.rerun()
