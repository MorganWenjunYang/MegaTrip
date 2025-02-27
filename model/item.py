import streamlit as st

class Item:
    def __init__(self, item_id, trip_id, name, description, date):
        self.item_id = item_id
        self.trip_id = trip_id
        self.name = name
        self.description = description
        self.date = date
        self.start_time = None  # new attribute for start time
        self.end_time = None  # new attribute for end time
        self.location = ""  # new attribute for location
        self.note = ""  # new attribute for note
        self.charge = 0.0  # new attribute for charge
        self.payer = None  # new attribute for payer
        self.split = {}  # new attribute for split

    def get_details(self):
        return {
            "item_id": self.item_id,
            "trip_id": self.trip_id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "start_time": self.start_time,  # include start time in details
            "end_time": self.end_time,  # include end time in details
            "location": self.location,  # include location in details
            "note": self.note,  # include note in details
            "charge": self.charge,  # include charge in details
            "payer": self.payer,  # include payer in details
            "split": self.split  # include split in details
        }

    def display_in_streamlit(self):
        """Display item details in Streamlit format"""
        with st.container():
            st.subheader(self.name)
            st.write(f"📅 Date: {self.date}")
            if self.start_time and self.end_time:
                st.write(f"⏰ Time: {self.start_time} - {self.end_time}")
            if self.location:
                st.write(f"📍 Location: {self.location}")
            if self.note:
                st.write(f"📝 Note: {self.note}")
            st.write(f"💰 Charge: ${self.charge}")
            if self.payer:
                st.write(f"💳 Payer: {self.payer}")
            if self.split:
                st.write(f"🔄 Split: {self.split}")