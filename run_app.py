#!/usr/bin/env python3
"""
Script to run both FastAPI and Streamlit applications
"""
import subprocess
import sys
import threading
import time
import uvicorn
from api.main import app

def run_fastapi():
    """Run FastAPI server"""
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def run_streamlit():
    """Run Streamlit server"""
    print("Starting Streamlit server on http://localhost:8501")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "main.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

if __name__ == "__main__":
    print("Starting MegaTrip application...")
    print("FastAPI will be available at: http://localhost:8000 (internal only)")
    print("FastAPI docs will be available at: http://localhost:8000/docs (internal only)")
    print("Streamlit will be available at: http://localhost:8501 (public)")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Give FastAPI a moment to start
    time.sleep(2)
    
    # Run Streamlit in the main thread
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\nShutting down applications...")
        sys.exit(0) 