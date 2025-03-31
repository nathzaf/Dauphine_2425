#!/bin/bash

# Specify the path where you want to create the virtual environment
VENV_DIR=".venv"

# Create the virtual environment
python -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install Jupyter Notebook and ipykernel inside the virtual environment
pip install jupyter ipykernel

# Create a kernel for the virtual environment
python -m ipykernel install --user --name=loreal-kernel

pip install --upgrade --quiet requests
pip install --upgrade --quiet pandas
pip install --upgrade --quiet pillow
pip install --upgrade --quiet matplotlib
pip install --upgrade --quiet google-cloud-storage
pip install -qU "langchain[cohere]"
pip install --upgrade --quiet langchain

# Display a message indicating successful setup
echo "##############################################################################################################"
echo "Virtual environment created and Jupyter kernel installed successfully."
echo "To use this environment in Jupyter Notebook, select 'genaiservices_kernel' as the kernel."
echo "##############################################################################################################"