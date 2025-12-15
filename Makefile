# Django Project Makefile
PYTHON = python3.13

# Django migrations
migrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

# Run development server
dev:
	$(PYTHON) manage.py runserver

# Create superuser
superuser:
	$(PYTHON) manage.py createsuperuser

# Collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput

# Run tests
test:
	$(PYTHON) manage.py test

# Shell access
shell:
	$(PYTHON) manage.py shell

# Database shell
dbshell:
	$(PYTHON) manage.py dbshell

# Check for issues
check:
	$(PYTHON) manage.py check

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete


# Run PostgreSQL Docker container (standalone)
run-db:
	docker run --name mykyta_db -e POSTGRES_DB=mykyta_db -e POSTGRES_USER=mykyta_admin -e POSTGRES_PASSWORD=CULZEP7ac0DgixnAgynW -p 5432:5432 -d postgres:18.1-alpine3.23

# Stop PostgreSQL Docker container (standalone)
stop-db:
	docker stop mykyta_db && docker rm mykyta_db

# Docker Compose commands
docker-up:
	docker compose up --build

docker-up-d:
	docker compose up --build -d

docker-down:
	docker compose down

docker-down-v:
	docker compose down -v

docker-logs:
	docker compose logs -f web

docker-shell:
	docker compose exec web uv run manage.py shell

docker-dbshell:
	docker compose exec db psql -U mykyta_admin -d mykyta_db

docker-migrate:
	docker compose exec web uv run manage.py migrate

docker-makemigrations:
	docker compose exec web uv run manage.py makemigrations

docker-superuser:
	docker compose exec web uv run manage.py createsuperuser

docker-restart:
	docker compose restart web


# Help
help:
	@echo "Available commands:"
	@echo "  make makemigrations  - Create new migrations"
	@echo "  make migrate         - Apply migrations"
	@echo "  make runserver       - Start development server"
	@echo "  make createsuperuser - Create admin user"
	@echo "  make collectstatic   - Collect static files"
	@echo "  make test            - Run tests"
	@echo "  make shell           - Open Django shell"
	@echo "  make dbshell         - Open database shell"
	@echo "  make check           - Check for issues"
	@echo "  make clean           - Remove .pyc files and __pycache__"

.PHONY: makemigrations migrate runserver createsuperuser collectstatic test shell dbshell check clean help


# Linting and Formatting commands
lint:
	@echo "🔍 Running ruff linter..."
	uv run ruff check

lint-fix:
	@echo "🔧 Running ruff linter with auto-fix..."
	uv run ruff check --fix

format:
	@echo "✨ Formatting code with ruff..."
	uv run ruff format

format-check:
	@echo "📋 Checking code formatting..."
	uv run ruff format --check

check: lint format-check
	@echo "✅ All checks complete! Review any errors above."

check-stats:
	@echo "📊 Linting statistics:"
	@uv run ruff check --statistics || true
	@echo ""
	@echo "📋 Format check:"
	@uv run ruff format --check || true

fix: lint-fix format
	@echo "✅ Code linted and formatted!"
