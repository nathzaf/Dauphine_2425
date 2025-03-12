import subprocess
import uvicorn
import os
from multiprocessing import Process
from rest.api import app

def run_uvicorn():
    PORT = int(os.getenv("PORT", 8000))  # Render définit un PORT dynamique
    uvicorn.run("rest.api:app", host="0.0.0.0", port=PORT, reload=True)

def run_streamlit():
    home_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_app/Home.py'))
    streamlit_port = int(os.getenv("STREAMLIT_PORT", 8501))  # Streamlit utilise 8501 par défaut
    subprocess.run(["streamlit", "run", home_py_path, "--server.address", "0.0.0.0", "--server.port", str(streamlit_port)])

if __name__ == "__main__":
    p1 = Process(target=run_uvicorn)
    p2 = Process(target=run_streamlit)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
