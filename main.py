import subprocess
import uvicorn
import os

from multiprocessing import Process

def run_uvicorn():
    uvicorn.run("rest.api:rest_api", host="127.0.0.1", port=8000)

def run_streamlit():
    # Construct the absolute path to Home.py
    home_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_app/Home.py'))
    subprocess.run(["streamlit", "run", home_py_path])

if __name__ == "__main__":
    p1 = Process(target=run_uvicorn)
    p2 = Process(target=run_streamlit)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()