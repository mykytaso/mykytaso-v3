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
	uv run gunicorn app.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8012

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

# Production database commands
# Runs on the production host (not inside the app container).
# POSTGRES_USER and POSTGRES_DB are read from the db container's own environment, so the credentials are never repeated here.
COMPOSE_PROD = docker compose -f docker-compose.production.yaml --env-file=.env

prod-db-backup:
	@mkdir -p backups
	@set -e; \
	OUT=backups/mykytaso_db_$$(date +%Y%m%d_%H%M%S).dump; \
	$(COMPOSE_PROD) exec -T db sh -c 'pg_dump -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -Fc --no-owner --no-acl' \
		> $$OUT.tmp || { rm -f $$OUT.tmp; exit 1; }; \
	mv $$OUT.tmp $$OUT; \
	echo "✅ Backup written to $$OUT ($$(du -h $$OUT | cut -f1))"

prod-db-restore:
	@test -n "$(DUMP)" || { echo "❌ Usage: make prod-db-restore DUMP=backups/<file>.dump"; exit 1; }
	@test -s "$(DUMP)" || { echo "❌ $(DUMP) is missing or empty"; exit 1; }
	$(COMPOSE_PROD) exec -T db sh -c 'pg_restore -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" --clean --if-exists --no-owner --no-acl' < $(DUMP)
	@echo "✅ Restored from $(DUMP)"

prod-dbshell:
	$(COMPOSE_PROD) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

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
