import streamlit as st
from model.trip import Trip
from model.trip_manager import TripManager
from controller.controller import handle_save_trip, handle_cancel_edit, handle_back_to_home
from viewer.stutils import show_sidebar, show_trip_details

def show_trip_details_page():
    show_sidebar()
    if st.session_state.current_trip_id:
        trip = TripManager.get_trip_by_id(st.session_state.current_trip_id)
        if trip:
            if 'edit_mode' not in st.session_state:
                st.session_state.edit_mode = False

            if st.session_state.edit_mode:
                st.header(f"Edit Trip: {trip.name}")
                
                with st.form("edit_trip_form"):
                    new_name = st.text_input("Trip Name", value=trip.name)
                    new_destination = st.text_input("Destination", value=trip.destination)
                    col1, col2 = st.columns(2)
                    with col1:
                        new_start_date = st.date_input("Start Date", value=trip.start_date)
                    with col2:
                        new_end_date = st.date_input("End Date", value=trip.end_date)
                    
                    new_status = st.selectbox(
                        "Status",
                        options=["Planning", "Ongoing", "Completed", "Cancelled"],
                        index=["Planning", "Ongoing", "Completed", "Cancelled"].index(trip.status)
                    )
                    
                    new_note = st.text_area("Notes", value=trip.note)
                    
                    # Item management
                    st.subheader("Items")
                    if not hasattr(trip, 'items'):
                        trip.items = []
                    
                    for idx, item in enumerate(trip.items):
                        st.text(f"• {item}")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        new_item = st.text_input("Add an item", key="new_item")
                    with col2:
                        add_item = st.form_submit_button("+ Add", type="secondary")
                        if add_item and new_item:
                            trip.items.append(new_item)
                            st.rerun()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save"):
                            handle_save_trip(trip, new_name, new_destination, new_start_date, 
                                          new_end_date, new_status, new_note)
                    with col2:
                        if st.form_submit_button("Cancel"):
                            handle_cancel_edit()
            else:
                show_trip_details(trip)
        else:
            st.error("Trip not found")
            handle_back_to_home()
    else:
        st.error("No trip selected")
        handle_back_to_home()