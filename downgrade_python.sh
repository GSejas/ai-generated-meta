#!/bin/bash

# Remove existing Python3
sudo apt-get remove python3

# Update package lists
sudo apt-get update

# Install Python 3.9
sudo apt-get install python3.9

# Check installed version
python3.9 --version

# Create a new virtual environment with Python 3.9
python3.9 -m venv new_venv

# Activate the virtual environment
source new_venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Run your project or any other command
# python your_project.py
