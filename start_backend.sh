#!/bin/bash
echo "Starting AI Voice Detection API..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000



