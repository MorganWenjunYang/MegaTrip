import streamlit as st
from datetime import datetime, time
from trip import Trip
from item import Item
from trip_manager import TripManager
from viewer.stutils import show_sidebar

def init_item():
    """Initialize an empty item with default values"""
    return {
        "name": "",
        "description": "",
        "date": datetime.today().date(),
        "start_time": time(9, 0),  # Default 9:00 AM
        "end_time": time(10, 0),   # Default 10:00 AM
        "location": "",
        "note": "",
        "charge": 0.0,
        "payer": "",
        "split": {}
    }

def show_create_trip_page():
    show_sidebar()
    st.header("Create New Trip")
    
    # Initialize items in session state
    if 'trip_items' not in st.session_state:
        st.session_state.trip_items = [init_item()]
    
    with st.form("new_trip_form"):
        # Basic trip info
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
        
        # Items section
        st.subheader("Items")
        
        for idx, item in enumerate(st.session_state.trip_items):
            with st.container():
                st.markdown(f"**Item {idx + 1}**")
                col1, col2 = st.columns(2)
                with col1:
                    item["name"] = st.text_input("Name", value=item["name"], key=f"name_{idx}")
                    item["description"] = st.text_area("Description", value=item["description"], key=f"desc_{idx}", height=100)
                    item["date"] = st.date_input("Date", value=item["date"], key=f"date_{idx}")
                with col2:
                    item["location"] = st.text_input("Location", value=item["location"], key=f"loc_{idx}")
                    item["note"] = st.text_area("Note", value=item["note"], key=f"note_{idx}", height=100)
                    item["charge"] = st.number_input("Charge ($)", value=item["charge"], key=f"charge_{idx}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    item["start_time"] = st.time_input("Start Time", value=item["start_time"], key=f"start_{idx}")
                with col2:
                    item["end_time"] = st.time_input("End Time", value=item["end_time"], key=f"end_{idx}")
                with col3:
                    item["payer"] = st.text_input("Payer", value=item["payer"], key=f"payer_{idx}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button(f"➕ Add Item {idx+1}"):
                        st.session_state.trip_items.insert(idx + 1, init_item())
                        st.rerun()
                with col2:
                    if len(st.session_state.trip_items) > 1 and st.form_submit_button(f"🗑️ Delete Item {idx+1}"):
                        st.session_state.trip_items.pop(idx)
                        st.rerun()
                
                st.markdown("---")
        
        # Form submission
        if st.form_submit_button("Create Trip"):
            if not name or not destination:
                st.error("Trip name and destination are required!")
                return
                
            if end_date < start_date:
                st.error("End date cannot be earlier than start date!")
                return
            
            # Convert items to proper Item objects
            items = []
            for idx, item_data in enumerate(st.session_state.trip_items):
                if item_data["name"]:  # Only include items with names
                    item = Item(
                        item_id=None,  # Will be set by database
                        trip_id=None,  # Will be set after trip creation
                        **item_data
                    )
                    items.append(item)
            
            new_trip = Trip(
                name=name,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                status=status,
                note=note,
                owner=st.session_state.username,
                items=items
            )
            
            TripManager.create_trip(new_trip)
            st.session_state.trip_items = [init_item()]  # Reset items
            st.success("Trip created successfully!")
            st.session_state.page = None
            st.rerun()
    
    if st.button("Cancel"):
        st.session_state.page = None
        st.rerun()
