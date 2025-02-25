import streamlit as st
from trip_manager import TripManager
from controller import handle_save_trip, handle_cancel_edit, handle_back_to_home

def show_trip_details_page():
    if st.session_state.current_trip_id:
        trip = TripManager.get_trip_by_id(st.session_state.current_trip_id)
        if trip:
            if 'edit_mode' not in st.session_state:
                st.session_state.edit_mode = False

            if st.session_state.edit_mode:
                st.title(f"Edit Trip: {trip.name}")
                new_name = st.text_input("Trip Name", value=trip.name)
                new_destination = st.text_input("Destination", value=trip.destination)
                new_start_date = st.date_input("Start Date", value=trip.start_date)
                new_end_date = st.date_input("End Date", value=trip.end_date)
                new_status = st.selectbox("Status", ["Active", "Planned", "Completed"], index=["Active", "Planned", "Completed"].index(trip.status))
                new_note = st.text_area("Note", value=trip.note)
                
                if st.button("Save"):
                    handle_save_trip(trip, new_name, new_destination, new_start_date, new_end_date, new_status, new_note)
                
                if st.button("Cancel"):
                    handle_cancel_edit()
            else:
                st.title(f"Trip Details: {trip.name}")
                st.write(f"🌍 Destination: {trip.destination}")
                st.write(f"📅 {trip.start_date} to {trip.end_date}")
                st.write(f"📌 Status: {trip.status}")
                if trip.note:
                    st.write(f"📝 Note: {trip.note}")
                if trip.participants:
                    st.write(f"👥 Participants: {', '.join(trip.participants)}")
                if trip.items:
                    st.write("📋 Items:")
                    for item in trip.items:
                        st.write(f"- {item.name}")
                
                if st.button("Edit"):
                    st.session_state.edit_mode = True
                
                if st.button("Back to Home"):
                    handle_back_to_home()
        else:
            st.error("Trip not found")
            handle_back_to_home()
    else:
        st.error("No trip selected")
        handle_back_to_home()