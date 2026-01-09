# Django Project Makefile

# Django migrations
migrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

# Create superuser
superuser:
	uv run manage.py createsuperuser

# Docker Compose commands
prod:
	uv run manage.py migrate
	cp -r /app/frontend/static /tmp/
	uv run gunicorn app.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8012 --capture-output --log-level debug --access-logfile - --error-logfile -

dev:
	docker compose -f docker-compose.yaml up

dev-rebuild:
	docker compose -f docker-compose.yaml up --build --force-recreate

docker-migrate:
	docker compose exec web uv run manage.py migrate

docker-makemigrations:
	docker compose exec web uv run manage.py makemigrations

docker-superuser:
	docker compose exec web uv run manage.py createsuperuser

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
