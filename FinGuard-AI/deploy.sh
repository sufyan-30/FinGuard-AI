#!/bin/bash
# FinGuard AI - Deployment Script

set -e

echo "=========================================="
echo "FinGuard AI - Deployment & Verification"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
echo -e "${YELLOW}Checking Python version...${NC}"
python --version

# Check Node
echo -e "${YELLOW}Checking Node version...${NC}"
node --version

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python -m venv venv
source venv/bin/activate || . venv/Scripts/activate

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -q -r requirements.txt

# Verify imports
echo -e "${YELLOW}Verifying backend imports...${NC}"
python -c "
from backend.database import engine, get_db, init_db, Vendor, Invoice, AuditLog
from backend.core import get_redis, redis_health_check
from backend.models import VendorResponse, InvoiceResponse, AnomalyDetectionResult
from backend.routers import vendors_router, invoices_router, audit_logs_router
from backend.services import vendor_service, invoice_service
from ml_models import anomaly_detector, risk_predictor, forecaster
from backend.main import app
print('✓ All backend imports successful')
"

# Install frontend dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
cd frontend && npm install --silent && cd ..

# Verify TypeScript compilation
echo -e "${YELLOW}Verifying TypeScript...${NC}"
cd frontend && npx tsc --noEmit 2>&1 | grep -i error || echo "✓ TypeScript check passed" && cd ..

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Setup Complete!"
echo "==========================================${NC}"

echo ""
echo -e "${YELLOW}Quick Start:${NC}"
echo "1. Backend:  uvicorn backend.main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo -e "${YELLOW}Or use Docker:${NC}"
echo "  docker-compose up -d"
echo ""
echo -e "${YELLOW}API Documentation:${NC}"
echo "  http://localhost:8000/api/docs"
echo ""
