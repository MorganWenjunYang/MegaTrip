from user import User
from utils import execute_query

class UserManager:
    @staticmethod
    def get_user(username, password):
        """Get a user by username and password from database"""
        query = """
            SELECT * FROM users WHERE username = %s AND password = %s
        """
        user_data = execute_query(query, (username, password))
        
        if not user_data or len(user_data) == 0:
            return None
        
        return user_data[0]
        
    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID from database"""
        query = """
            SELECT * FROM users WHERE user_id = %s
        """
        user_data = execute_query(query, (user_id,))
        
        if not user_data or len(user_data) == 0:
            return None
        
        return user_data[0]
    
    @staticmethod
    def get_user_by_name(username):
        """Get a user by username from database"""
        query = """
            SELECT * FROM users WHERE username = %s
        """
        user_data = execute_query(query, (username,))
        
        if not user_data or len(user_data) == 0:
            return None
        
        return user_data[0]
    
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
    
