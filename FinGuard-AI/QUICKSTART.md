# FinGuard AI - Quick Start Guide

## System Overview

FinGuard AI is a production-grade fintech platform with:
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL + Redis
- **Frontend**: Next.js 14 + Tailwind CSS
- **ML Pipeline**: Anomaly Detection (Isolation Forest), Risk Prediction (XGBoost)
- **Real-time**: Async/await, connection pooling, caching

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

## 5-Minute Setup (Docker)

```bash
# 1. Navigate to project
cd C:\Users\pcJAWAD\FinGuard-AI

# 2. Start all services
docker-compose up -d

# 3. Verify health
curl http://localhost:8000/health

# 4. Access UI
# API Docs: http://localhost:8000/api/docs
# Frontend: http://localhost:3000
```

## Local Development Setup

### Backend

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Start PostgreSQL & Redis locally or via Docker
docker-compose up -d postgres redis

# 5. Initialize database
python -c "import asyncio; from backend.database import init_db; asyncio.run(init_db())"

# 6. Start FastAPI server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# 4. Start dev server
npm run dev
```

## API Endpoints

### Vendors
- `POST /api/vendors` - Create vendor
- `GET /api/vendors` - List vendors (paginated)
- `GET /api/vendors/{id}` - Get vendor
- `PUT /api/vendors/{id}` - Update vendor
- `DELETE /api/vendors/{id}` - Delete vendor

### Invoices
- `POST /api/invoices` - Create invoice (with ML detection)
- `GET /api/invoices` - List invoices (filterable)
- `GET /api/invoices/{id}` - Get invoice
- `PUT /api/invoices/{id}` - Update invoice
- `POST /api/invoices/{id}/detect-anomaly` - Re-run anomaly detection

### Audit Logs
- `GET /api/audit-logs` - List audit logs (paginated)
- `GET /api/audit-logs/vendor/{vendor_id}` - Vendor audit logs

### Health
- `GET /health` - System health check

## Frontend Routes

- `/` - Dashboard (system status)
- `/vendors` - Vendor management
- `/invoices` - Invoice tracking & anomaly detection
- `/audit` - Audit log viewer

## ML Models

### Anomaly Detection
- **Model**: Isolation Forest
- **Features**: Invoice amount, payment days, vendor risk
- **Output**: Boolean + confidence score

### Risk Prediction
- **Model**: XGBoost
- **Features**: Same as anomaly detection
- **Output**: Late payment probability (0-1)

### Forecasting
- **Model**: Linear Regression
- **Features**: Historical trends
- **Output**: Payment forecast

## Database Schema

### Vendors
```sql
- id (PK)
- name (unique, indexed)
- email
- phone
- country
- risk_score (0-100)
- created_at, updated_at
```

### Invoices
```sql
- id (PK)
- vendor_id (FK)
- amount (decimal)
- issue_date, due_date
- status (pending|paid|overdue|disputed)
- is_anomaly (bool)
- late_risk_probability (0-1)
- created_at, updated_at
```

### AuditLogs
```sql
- id (PK)
- vendor_id (FK)
- invoice_id (FK)
- action (string)
- model_type (string)
- prediction (float)
- confidence (float)
- details (text)
- created_at
```

## Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

## Troubleshooting

**API Connection Failed**
- Check `CORS_ORIGINS` in `.env`
- Verify PostgreSQL is running: `docker-compose ps`
- Check logs: `docker-compose logs fastapi`

**Frontend Not Loading Data**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check browser console for errors
- Run `curl http://localhost:8000/health`

**Database Errors**
- Reset: `docker-compose down -v && docker-compose up -d`
- Check connection string in `.env`

## Production Deployment

See `docs/DEPLOYMENT.md` for:
- Kubernetes setup
- AWS EC2 deployment
- CI/CD pipeline
- Monitoring & alerting

## Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DB_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Key Features

✅ Async/await throughout  
✅ Connection pooling (DB: 20, Redis: 20)  
✅ CORS configured  
✅ Real-time ML predictions  
✅ Audit logging  
✅ Type hints (100% coverage)  
✅ Production-ready error handling  
✅ Health checks  

## Next Steps

1. Start services: `docker-compose up -d`
2. Access API docs: http://localhost:8000/api/docs
3. Create sample vendors & invoices
4. Monitor predictions in audit logs
5. Deploy to production (see docs/)

## Support

- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Database: PostgreSQL 16
- Cache: Redis 7
