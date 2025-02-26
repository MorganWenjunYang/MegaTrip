from user import User
from utils import execute_query

class UserManager:
    
    @staticmethod
    def create_user(username, password):
        """Create a new user in the database"""
        query = """
            INSERT INTO users (username, password) VALUES (%s, %s)
        """
        user_id = execute_query(query, (username, password), fetch=False)
        return user_id
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user from the database"""
        query = """
            DELETE FROM users WHERE user_id = %s
        """
        execute_query(query, (user_id,), fetch=False)
    
    