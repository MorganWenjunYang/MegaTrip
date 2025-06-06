from streamlit.web.server.server import Server
import streamlit as st
import os

def create_streamlit_app():
    # Create and start streamlit server
    server = Server()
    
    # Configure the server
    server._start_server = lambda *args, **kwargs: None  # Prevent auto-start
    
    # Load your Streamlit app
    import main
    
    return server.app

# Create WSGI application
app = create_streamlit_app() 