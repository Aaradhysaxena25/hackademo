.PHONY: setup dev migrate test lint format clean

# Setup project dependencies
setup:
	cd backend && pip install -r requirements/development.txt
	cd frontend && npm install

# Start development environment with Docker
dev:
	docker-compose up -d

# Stop development environment
down:
	docker-compose down

# Run database migrations
migrate:
	cd backend && python manage.py makemigrations
	cd backend && python manage.py migrate

# Run backend tests
test:
	cd backend && pytest

# Run linter
lint:
	cd backend && ruff check .

# Format code
format:
	cd backend && ruff format .

# Create superuser
superuser:
	cd backend && python manage.py createsuperuser

# Clean up generated files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/.pytest_cache backend/htmlcov backend/.coverage
