import streamlit as st
from trip_manager import TripManager

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
                    trip.name = new_name
                    trip.destination = new_destination
                    trip.start_date = new_start_date
                    trip.end_date = new_end_date
                    trip.status = new_status
                    trip.note = new_note
                    TripManager.update_trip(trip)
                    st.session_state.edit_mode = False
                    st.success("Trip details updated successfully")
                
                if st.button("Cancel"):
                    st.session_state.edit_mode = False
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
                    st.session_state.page = "home"
                    st.session_state.current_trip_id = None
        else:
            st.error("Trip not found")
            st.session_state.page = "home"
    else:
        st.error("No trip selected")
        st.session_state.page = "home"