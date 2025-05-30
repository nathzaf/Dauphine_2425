import subprocess
import uvicorn
import os
import time
from multiprocessing import Process

def run_uvicorn():
    uvicorn.run("rest.api:rest_api", host="127.0.0.1", port=8000)

def run_streamlit():
    # Wait a bit for the backend to start
    time.sleep(3)
    # Construct the absolute path to Home.py
    home_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_app/Home.py'))
    subprocess.run(["streamlit", "run", home_py_path])

if __name__ == "__main__":
    print("Starting backend...")
    p1 = Process(target=run_uvicorn)
    p1.start()
    
    print("Starting frontend...")
    p2 = Process(target=run_streamlit)
    p2.start()
    
    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("Shutting down...")
        p1.terminate()
        p2.terminate()