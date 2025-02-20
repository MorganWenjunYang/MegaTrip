class Trip:
    def __init__(self, trip_id, name, destination, start_date, end_date, creator_id):
        self.trip_id = trip_id
        self.name = name
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
        self.participants = []
        self.items = []  # list of activities/items in the trip

    def add_participant(self, user):
        """Add a participant to the trip"""
        if user not in self.participants:
            self.participants.append(user)
            return True
        return False

    def remove_participant(self, user):
        """Remove a participant from the trip"""
        if user in self.participants:
            self.participants.remove(user)
            return True
        return False

    def add_item(self, item):
        """Add an activity/item to the trip"""
        self.items.append(item)

    def remove_item(self, item):
        """Remove an activity/item from the trip"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_details(self):
        """Get all details about the trip"""
        return {
            "trip_id": self.trip_id,
            "name": self.name,
            "destination": self.destination,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "creator_id": self.creator_id,
            "participants": [user.name for user in self.participants],
            "items": [item.get_details() for item in self.items]
        }
     
    def display_in_streamlit(self):
        """Display trip details in Streamlit format"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(self.name)
                st.write(f"🌍 Destination: {self.destination}")
                st.write(f"📅 {self.start_date} to {self.end_date}")
                if self.participants:
                    st.write(f"👥 Participants: {', '.join([p.name for p in self.participants])}")
            with col2:
                if st.button("View Details", key=f"trip_{self.trip_id}"):
                    st.session_state.current_trip = self.trip_id
                    st.session_state.page = "trip_details"