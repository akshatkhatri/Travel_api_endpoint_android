#!/bin/bash

# Activate your virtual environment
source travel_api_venv/bin/activate

# Run Gunicorn with your Flask app
gunicorn app:app --bind 0.0.0.0:8000 --workers 4
chmod +x start.sh
