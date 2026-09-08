# FinGuard AI Development Makefile
# Convenient commands for development, testing, and deployment

.PHONY: help install dev test lint format clean docker-up docker-down db-migrate db-rollback

help:
	@echo "FinGuard AI - Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run              Run development server"
	@echo "  make test             Run tests with coverage"
	@echo "  make test-fast        Run tests without coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run all linters (flake8, mypy, pylint)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make check            Run lint and format checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        Start Docker Compose services"
	@echo "  make docker-down      Stop Docker Compose services"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-logs      View Docker logs"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate       Run database migrations"
	@echo "  make db-rollback      Rollback last migration"
	@echo "  make db-new           Create new migration"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and cache"
	@echo "  make clean-all        Clean everything including venv"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install -e ".[dev]"

run:
	@echo "Starting development server..."
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=backend --cov-report=html --cov-report=term-missing

test-fast:
	@echo "Running tests (fast)..."
	pytest tests/ -v

lint:
	@echo "Running linters..."
	flake8 backend/ tests/
	mypy backend/
	pylint backend/

format:
	@echo "Formatting code..."
	black backend/ tests/
	isort backend/ tests/

check:
	@echo "Running code checks..."
	black --check backend/ tests/
	isort --check-only backend/ tests/
	flake8 backend/ tests/

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/api/docs"
	@echo "Health: http://localhost:8000/health"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

docker-build:
	@echo "Building Docker image..."
	docker build -t finguard-ai:latest .

docker-logs:
	docker-compose logs -f

db-migrate:
	@echo "Running database migrations..."
	alembic upgrade head

db-rollback:
	@echo "Rolling back last migration..."
	alembic downgrade -1

db-new:
	@echo "Creating new migration..."
	alembic revision --autogenerate -m "$(MSG)"

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf venv/

.DEFAULT_GOAL := help
