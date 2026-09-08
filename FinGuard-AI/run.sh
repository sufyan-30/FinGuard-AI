#!/bin/bash
# FinGuard AI Backend Startup Script

cd "$(dirname "$0")" || exit

echo "Starting FinGuard AI Backend..."

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "
import asyncio
from backend.database import init_db
asyncio.run(init_db())
"

# Start FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
