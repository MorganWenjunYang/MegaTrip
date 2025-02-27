import streamlit as st

class Trip:
    def __init__(self, trip_id, name, destination, start_date, end_date, creator_id):
        self.trip_id = trip_id
        self.name = name
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
        self.participants = []  # list of user IDs
        self.items = []  # list of activities/items in the trip
        self.status = "Active"  # new attribute for trip status
        self.note = ""  # new attribute for trip note

    def add_participant(self, user_id):
        """Add a participant to the trip"""
        if user_id not in self.participants:
            self.participants.append(user_id)
            return True
        return False

    def remove_participant(self, user_id):
        """Remove a participant from the trip"""
        if user_id in self.participants:
            self.participants.remove(user_id)
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
            "participants": self.participants,  # list of user IDs
            "items": [item.get_details() for item in self.items],
            "status": self.status,  # include status in details
            "note": self.note  # include note in details
        }
     
    