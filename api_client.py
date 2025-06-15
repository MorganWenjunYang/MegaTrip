import requests
from typing import List, Dict, Optional
import streamlit as st
import os

class APIClient:
    def __init__(self, base_url: str = None):
        # Use environment variable if available (for Docker), otherwise default to localhost
        if base_url is None:
            base_url = os.getenv('API_URL', 'http://localhost:8000')
        self.base_url = base_url
        self.session = requests.Session()
    
    def _handle_response(self, response: requests.Response):
        """Handle API response and raise exceptions for errors"""
        if response.status_code >= 400:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = response.text
            st.error(f"API Error: {error_detail}")
            return None
        return response.json()
    
    # User methods
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Login user"""
        response = self.session.post(
            f"{self.base_url}/api/users/login",
            json={"username": username, "password": password}
        )
        return self._handle_response(response)
    
    def create_user(self, username: str, password: str) -> Optional[Dict]:
        """Create new user"""
        response = self.session.post(
            f"{self.base_url}/api/users/",
            json={"username": username, "password": password}
        )
        return self._handle_response(response)
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        response = self.session.get(f"{self.base_url}/api/users/{user_id}")
        return self._handle_response(response)
    
    # Trip methods
    def create_trip(self, trip_data: Dict) -> Optional[Dict]:
        """Create new trip"""
        response = self.session.post(
            f"{self.base_url}/api/trips/",
            json=trip_data
        )
        return self._handle_response(response)
    
    def get_trip(self, trip_id: int) -> Optional[Dict]:
        """Get trip by ID with full details"""
        response = self.session.get(f"{self.base_url}/api/trips/{trip_id}")
        return self._handle_response(response)
    
    def update_trip(self, trip_id: int, trip_data: Dict) -> Optional[Dict]:
        """Update trip"""
        response = self.session.put(
            f"{self.base_url}/api/trips/{trip_id}",
            json=trip_data
        )
        return self._handle_response(response)
    
    def delete_trip(self, trip_id: int) -> bool:
        """Delete trip"""
        response = self.session.delete(f"{self.base_url}/api/trips/{trip_id}")
        result = self._handle_response(response)
        return result is not None
    
    def get_recent_trips(self, limit: int = 10) -> List[Dict]:
        """Get recent trips"""
        response = self.session.get(f"{self.base_url}/api/trips/?limit={limit}")
        result = self._handle_response(response)
        return result if result else []
    
    def get_user_created_trips(self, user_id: int) -> List[Dict]:
        """Get trips created by user"""
        response = self.session.get(f"{self.base_url}/api/users/{user_id}/created-trips")
        result = self._handle_response(response)
        return result if result else []
    
    def get_user_participated_trips(self, user_id: int) -> List[Dict]:
        """Get trips user participated in"""
        response = self.session.get(f"{self.base_url}/api/users/{user_id}/participated-trips")
        result = self._handle_response(response)
        return result if result else []
    
    def add_trip_participant(self, trip_id: int, user_id: int) -> bool:
        """Add participant to trip"""
        response = self.session.post(f"{self.base_url}/api/trips/{trip_id}/participants/{user_id}")
        result = self._handle_response(response)
        return result is not None
    
    def remove_trip_participant(self, trip_id: int, user_id: int) -> bool:
        """Remove participant from trip"""
        response = self.session.delete(f"{self.base_url}/api/trips/{trip_id}/participants/{user_id}")
        result = self._handle_response(response)
        return result is not None
    
    # Item methods
    def create_item(self, item_data: Dict) -> Optional[Dict]:
        """Create new item"""
        response = self.session.post(
            f"{self.base_url}/api/items/",
            json=item_data
        )
        return self._handle_response(response)
    
    def get_item(self, item_id: int) -> Optional[Dict]:
        """Get item by ID"""
        response = self.session.get(f"{self.base_url}/api/items/{item_id}")
        return self._handle_response(response)
    
    def update_item(self, item_id: int, item_data: Dict) -> Optional[Dict]:
        """Update item"""
        response = self.session.put(
            f"{self.base_url}/api/items/{item_id}",
            json=item_data
        )
        return self._handle_response(response)
    
    def delete_item(self, item_id: int) -> bool:
        """Delete item"""
        response = self.session.delete(f"{self.base_url}/api/items/{item_id}")
        result = self._handle_response(response)
        return result is not None
    
    def get_trip_items(self, trip_id: int) -> List[Dict]:
        """Get all items for a trip"""
        response = self.session.get(f"{self.base_url}/api/trips/{trip_id}/items")
        result = self._handle_response(response)
        return result if result else []

# Global API client instance
api_client = APIClient() 