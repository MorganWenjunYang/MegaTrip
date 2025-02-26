from item import Item
from utils import execute_query

class ItemManager:
    
    @staticmethod
    def get_items_by_trip(trip_id):
        """Get all items for a trip from database"""
        query = """
            SELECT * FROM items WHERE trip_id = %s
        """
        items_data = execute_query(query, (trip_id,))
        
        # Convert database records to Item objects
        items = []
        for data in items_data:
            item = Item(
                item_id=data['item_id'],
                name=data['name'],
                quantity=data['quantity'],
                trip_id=data['trip_id']
            )
            items.append(item)
        
        return items
    
    @staticmethod
    def create_item(name, quantity, trip_id):
        """Create a new item in the database"""
        query = """
            INSERT INTO items (name, quantity, trip_id) VALUES (%s, %s, %s)
        """
        item_id = execute_query(query, (name, quantity, trip_id), fetch=False)
        return item_id
    
    @staticmethod
    def update_item(item):
        """Update an item in the database"""
        query = """
            UPDATE items SET name=%s, quantity=%s WHERE item_id=%s
        """
        execute_query(query, (item.name, item.quantity, item.item_id), fetch=False)

    @staticmethod
    def delete_item(item_id):
        """Delete an item from the database"""
        query = """
            DELETE FROM items WHERE item_id = %s
        """
        execute_query(query, (item_id,), fetch=False)