import subprocess
import uvicorn
import os

from multiprocessing import Process

def run_uvicorn():
PORT = int(os.getenv("PORT", 8000))  # Render définit un PORT dynamique
uvicorn.run("rest.api:rest_api", host="0.0.0.0", port=PORT)

def run_streamlit():
    # Construct the absolute path to Home.py
    PORT = int(os.getenv("PORT", 8501))  # Streamlit utilise 8501 par défaut
    subprocess.run(["streamlit", "run", home_py_path, "--server.address", "0.0.0.0", "--server.port", str(PORT)])

if __name__ == "__main__":
    p1 = Process(target=run_uvicorn)
    p2 = Process(target=run_streamlit)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
