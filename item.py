class Item:
    def __init__(self, item_id, trip_id, name, description, date):
        self.item_id = item_id
        self.trip_id = trip_id
        self.name = name
        self.description = description
        self.date = date

    def get_details(self):
        return {
            "item_id": self.item_id,
            "trip_id": self.trip_id,
            "name": self.name,
            "description": self.description,
            "date": self.date
        }