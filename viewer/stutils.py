import streamlit as st
from api_client import api_client
from datetime import datetime, time

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

def init_trip():
    """Initialize an empty trip with default values"""
    return {
        "name": "",
        "destination": "",
        "start_date": datetime.today().date(),
        "end_date": datetime.today().date(),
        "status": "Active",
        "note": "",
        "items": []
    }

def handle_cancel_edit():
    """Cancel edit mode and clean up session state"""
    st.session_state.edit_mode = False
    if 'staged_trip' in st.session_state:
        del st.session_state.staged_trip
    st.rerun()

def handle_back_to_home():
    """Navigate back to home page and clean up session state"""
    st.session_state.page = "home"
    st.session_state.current_trip_id = None
    if 'staged_trip' in st.session_state:
        del st.session_state.staged_trip
    if 'edit_mode' in st.session_state:
        del st.session_state.edit_mode
    st.rerun()

def handle_input_check(staged):
    """Validate trip input data"""
    if not staged:
        st.warning("Please fill in all required fields")
        return False

    if not staged['start_date'] or not staged['end_date']:
        st.warning("Please select a start and end date")
        return False

    if staged['start_date'] > staged['end_date']:
        st.warning("End date must be after start date")
        return False

    if not staged['destination']:
        st.warning("Please enter a destination")
        return False

    if not staged['status']:
        st.warning("Please enter a status")
        return False

    return True

def handle_save_trip(staged):
    """Save new trip using API client"""
    if not handle_input_check(staged):
        return

    # Prepare trip data for API
    trip_data = {
        "name": staged['name'],
        "destination": staged['destination'],
        "start_date": staged['start_date'].isoformat(),
        "end_date": staged['end_date'].isoformat(),
        "status": staged['status'],
        "note": staged['note'],
        "creator_id": st.session_state.user_id
    }
    
    result = api_client.create_trip(trip_data)
    if result:
        # Create items for the trip
        for item in staged['items']:
            if item['name']:  # Only create items with names
                item_data = {
                    "trip_id": result['trip_id'],
                    "name": item['name'],
                    "description": item['description'],
                    "date": item['date'].isoformat() if item['date'] else None,
                    "start_time": item['start_time'].isoformat() if item['start_time'] else None,
                    "end_time": item['end_time'].isoformat() if item['end_time'] else None,
                    "location": item['location'],
                    "note": item['note'],
                    "charge": float(item['charge']),
                    "payer": item['payer']
                }
                api_client.create_item(item_data)
        
        st.session_state.edit_mode = False
        if 'staged_trip' in st.session_state:
            del st.session_state.staged_trip
        st.session_state.page = "home"
        st.session_state.current_trip_id = None
        st.success("Trip created successfully!")
        st.rerun()

def handle_update_trip(staged):
    """Update existing trip using API client"""
    if not handle_input_check(staged):
        return

    # Prepare trip data for API
    trip_data = {
        "name": staged['name'],
        "destination": staged['destination'],
        "start_date": staged['start_date'].isoformat(),
        "end_date": staged['end_date'].isoformat(),
        "status": staged['status'],
        "note": staged['note']
    }
    
    result = api_client.update_trip(st.session_state.current_trip_id, trip_data)
    if result:
        # Delete existing items and recreate them
        existing_items = api_client.get_trip_items(st.session_state.current_trip_id)
        for item in existing_items:
            api_client.delete_item(item['item_id'])
        
        # Create new items
        for item in staged['items']:
            if item['name']:  # Only create items with names
                item_data = {
                    "trip_id": st.session_state.current_trip_id,
                    "name": item['name'],
                    "description": item['description'],
                    "date": item['date'].isoformat() if item['date'] else None,
                    "start_time": item['start_time'].isoformat() if item['start_time'] else None,
                    "end_time": item['end_time'].isoformat() if item['end_time'] else None,
                    "location": item['location'],
                    "note": item['note'],
                    "charge": float(item['charge']),
                    "payer": item['payer']
                }
                api_client.create_item(item_data)
        
        st.session_state.edit_mode = False
        if 'staged_trip' in st.session_state:
            del st.session_state.staged_trip
        st.session_state.page = "home"
        st.session_state.current_trip_id = None
        st.success("Trip updated successfully!")
        st.rerun()

def show_sidebar():
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home", key="home", use_container_width=True):
            handle_back_to_home()
        if st.button("Profile", key="profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

def show_trip_edit(trip):
    pass

def show_trip_details(trip):
    st.title(f"Trip Details: {trip['name']}")
    st.write(f"🌍 Destination: {trip['destination']}")
    st.write(f"📅 {trip['start_date']} to {trip['end_date']}")
    st.write(f"📌 Status: {trip['status']}")
    if trip.get('note'):
        st.write(f"📝 Note: {trip['note']}")
    if trip.get('participants'):
        participant_names = [p['username'] for p in trip['participants']]
        st.write(f"👥 Participants: {', '.join(participant_names)}")
    if trip.get('items'):
        st.write("📋 Items:")
        for item in trip['items']:
            st.write(f"- {item['name']}")
    
    if st.button("Edit"):
        st.session_state.edit_mode = True
        st.rerun()
    
    if st.button("Back to Home"):
        handle_back_to_home()

def show_trip_short(trip):
    """Display trip details in Streamlit format"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(trip['name'])
            st.write(f"🌍 Destination: {trip['destination']}")
            st.write(f"📅 {trip['start_date']} to {trip['end_date']}")
            st.write(f"📌 Status: {trip['status']}")
            if trip.get('note'):
                st.write(f"📝 Note: {trip['note']}")
        with col2:
            if st.button("View Details", key=f"trip_{trip['trip_id']}"):
                st.session_state.current_trip_id = trip['trip_id']
                st.session_state.page = "trip_details"
                st.rerun()

def show_trip_expander(trips, context="default"):
    for trip in trips:
        with st.expander(f"🎯 {trip['name']} ({trip['destination']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dates:** {trip['start_date']} - {trip['end_date']}")
                st.write(f"**Status:** {trip['status']}")
            with col2:
                if trip.get('note'):
                    st.write(f"**Note:** {trip['note']}")
            
            # Make key unique by including context
            if st.button("View Details", key=f"{context}_view_{trip['trip_id']}"):
                st.session_state.current_trip_id = trip['trip_id']
                st.session_state.page = "trip_details"
                st.rerun()

def edit_trip(trip=None):
    # Initialize staged changes in session state if not exists
    if trip is None:
        st.session_state.staged_trip = init_trip()
    else:
        # Convert API response (dict) to staged format
        items_data = []
        if trip.get('items'):
            for item in trip['items']:
                item_dict = {
                    'name': item['name'],
                    'description': item['description'],
                    'date': datetime.fromisoformat(item['date']).date() if item['date'] else datetime.today().date(),
                    'start_time': datetime.fromisoformat(f"2000-01-01T{item['start_time']}").time() if item['start_time'] else time(9, 0),
                    'end_time': datetime.fromisoformat(f"2000-01-01T{item['end_time']}").time() if item['end_time'] else time(10, 0),
                    'location': item.get('location', ''),
                    'note': item.get('note', ''),
                    'charge': float(item.get('charge', 0.0)),
                    'payer': item.get('payer', ''),
                    'split': item.get('split', {})
                }
                items_data.append(item_dict)
        
        st.session_state.staged_trip = {
            'name': trip['name'],
            'destination': trip['destination'],
            'start_date': datetime.fromisoformat(trip['start_date']).date(),
            'end_date': datetime.fromisoformat(trip['end_date']).date(),
            'status': trip['status'],
            'note': trip.get('note', ''),
            'items': items_data
        }
    
    staged = st.session_state.staged_trip

    if trip is None:
        st.header("Create New Trip")
    else:
        st.header(f"Edit Trip: {trip['name']}")
                
    with st.form("edit_trip_form"):
        staged['name'] = st.text_input("Trip Name", value=staged['name'])
        staged['destination'] = st.text_input("Destination", value=staged['destination'])
        col1, col2 = st.columns(2)
        with col1:
            staged['start_date'] = st.date_input("Start Date", value=staged['start_date'])
        with col2:
            staged['end_date'] = st.date_input("End Date", value=staged['end_date'])
        
        staged['status'] = st.selectbox(
            "Status",
            options=["Active", "Completed", "Closed"],
            index=["Active", "Completed", "Closed"].index(staged['status'])
        )
        
        staged['note'] = st.text_area("Notes", value=staged['note'])
        
        # Items section
        st.subheader("Items")
        
        for idx, item in enumerate(staged['items']):
            with st.container():
                st.markdown(f"**Item {idx + 1}**")
                col1, col2 = st.columns(2)
                with col1:
                    item["name"] = st.text_input("Name", value=item['name'], key=f"name_{idx}")
                    item["description"] = st.text_area("Description", value=item['description'], key=f"desc_{idx}", height=100)
                    item["date"] = st.date_input("Date", value=item['date'], key=f"date_{idx}")
                with col2:
                    item["location"] = st.text_input("Location", value=item['location'], key=f"loc_{idx}")
                    item["note"] = st.text_area("Note", value=item['note'], key=f"note_{idx}", height=100)
                    item["charge"] = st.number_input("Charge ($)", value=item['charge'], key=f"charge_{idx}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    item["start_time"] = st.time_input("Start Time", value=item['start_time'], key=f"start_{idx}")
                with col2:
                    item["end_time"] = st.time_input("End Time", value=item['end_time'], key=f"end_{idx}")
                with col3:
                    item["payer"] = st.text_input("Payer", value=item['payer'], key=f"payer_{idx}")
                
                col1, col2 = st.columns(2)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Item {idx+1}"):
                        staged['items'].pop(idx)
                        st.rerun()
                
                st.markdown("---")

        # Always show an "Add Item" button at the bottom
        if st.form_submit_button("➕ Add New Item"):
            staged['items'].append(init_item())
            st.rerun()
        
        # Horizontal line before save/cancel buttons
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save"):
                if trip is None:
                    handle_save_trip(staged)
                else:
                    handle_update_trip(staged)
        with col2:
            if st.form_submit_button("Cancel"):
                handle_cancel_edit()

    
    