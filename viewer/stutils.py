import streamlit as st
from controller.controller import handle_save_trip, handle_cancel_edit, handle_back_to_home, handle_update_trip
from model.utils import init_item, init_trip

def show_sidebar():
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home", key="home", use_container_width=True):
            st.session_state.page = None
            st.rerun()
        if st.button("Profile", key="profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()


def show_trip_edit(trip):
    pass

def show_trip_details(trip):
    st.title(f"Trip Details: {trip.name}")
    st.write(f"🌍 Destination: {trip.destination}")
    st.write(f"📅 {trip.start_date} to {trip.end_date}")
    st.write(f"📌 Status: {trip.status}")
    if trip.note:
        st.write(f"📝 Note: {trip.note}")
    if trip.participants:
        st.write(f"👥 Participants: {', '.join([u.username for u in trip.participants])}")
    if trip.items:
        st.write("📋 Items:")
        for item in trip.items:
            st.write(f"- {item.name}")
    
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
                st.subheader(trip.name)
                st.write(f"🌍 Destination: {trip.destination}")
                st.write(f"📅 {trip.start_date} to {trip.end_date}")
                st.write(f"📌 Status: {trip.status}")  # display status
                if trip.note:
                    st.write(f"📝 Note: {trip.note}")  # display note if available
                # if trip.participants:
                    # st.write(f"👥 Participants: {', '.join(trip.participants)}")  # display user IDs
            with col2:
                if st.button("View Details", key=f"trip_{trip.trip_id}"):
                    st.session_state.current_trip_id = trip.trip_id
                    st.session_state.page = "trip_details"
                    st.rerun()

def show_trip_expander(trips, context="default"):
    for trip in trips:
        with st.expander(f"🎯 {trip.name} ({trip.destination})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dates:** {trip.start_date} - {trip.end_date}")
                st.write(f"**Status:** {trip.status}")
            with col2:
                if trip.note != '':
                    st.write(f"**Note:** {trip.note}")
            
            # Make key unique by including context
            if st.button("View Details", key=f"{context}_view_{trip.trip_id}"):
                st.session_state.current_trip_id = trip.trip_id
                st.session_state.page = "trip_details"
                st.rerun()


def edit_trip(trip=None):
        
    # Initialize staged changes in session state if not exists
    
    if trip is None:
        st.session_state.staged_trip = init_trip()
    else:
        st.session_state.staged_trip = {
            'name': trip.name,
            'destination': trip.destination,
            'start_date': trip.start_date,
            'end_date': trip.end_date,
            'status': trip.status,
            'note': trip.note,
            'items': [item.__dict__.copy() for item in trip.items]
        }
    
    staged = st.session_state.staged_trip

    if trip is None:
        st.header("Create New Trip")
    else:
        st.header(f"Edit Trip: {trip.name}")
                
    with st.form("edit_trip_form"):
        staged['name'] = st.text_input("Trip Name", value=staged['name'])
        staged['destination'] = st.text_input("Destination", value=staged['destination'])
        col1, col2 = st.columns(2)
        with col1:
            staged['start_date'] = st.date_input("Start Date", value=staged['start_date'])
        with col2:
            staged['end_date'] = st.date_input("End Date", value=staged['end_date'])
        
        new_status = st.selectbox(
            "Status",
            options=["Active", "Completed", "Closed"],
            index=["Active", "Completed", "Closed"].index(staged['status'])
        )
        
        new_note = st.text_area("Notes", value=staged['note'])
        
        # Item management
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
                with col1:
                    # if st.form_submit_button(f"➕ Add Item {idx+1}"):
                    #     staged['items'].insert(idx + 1, init_item())
                    #     st.rerun()
                    pass
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

    
    