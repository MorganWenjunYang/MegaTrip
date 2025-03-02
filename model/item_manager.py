from model.item import Item
from model.utils import execute_query, ModelConverter

class ItemManager:
    
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