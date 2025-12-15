# Mykytaso app V3

A Django 6.0+ web application with PostgreSQL backend, featuring user authentication and blog post management.

## Quick Start with Docker

The easiest way to run the application is using Docker Compose:

```bash
# Start both database and web server
make docker-up-d

# The application will be available at http://localhost:8000

# Create a superuser (optional)
make docker-superuser

# Stop the application
make docker-down
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)
- Make

### Running with Docker (Recommended)

1. Clone the repository
2. Create a `.env` file with your environment variables (see Environment Configuration below)
3. Start the application:

```bash
make docker-up-d
```

The dev server will automatically:
- Wait for PostgreSQL to be ready
- Run database migrations
- Start on http://localhost:8000

### Running Locally

If you prefer to run Django locally:

1. Start PostgreSQL in Docker:
```bash
make run-db
```

2. Install dependencies:
```bash
uv pip install -r pyproject.toml
```

3. Run migrations:
```bash
make migrate
```

4. Start the dev server:
```bash
make dev
```

### Environment Configuration

Create a `.env` file in the project root with:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
POSTGRES_DB=mykyta_db
POSTGRES_USER=mykyta_admin
POSTGRES_PASSWORD=CULZEP7ac0DgixnAgynW
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Useful Commands

### Docker Commands

```bash
make docker-up          # Start in foreground
make docker-up-d        # Start in background
make docker-down        # Stop all services
make docker-down-v      # Stop and remove volumes
make docker-logs        # View logs
make docker-shell       # Django shell
make docker-migrate     # Run migrations
make docker-superuser   # Create admin user
```

### Local Development Commands

```bash
make dev               # Start dev server
make migrate           # Run migrations
make shell             # Django shell
make test              # Run tests
make check             # Code quality checks
make fix               # Auto-fix linting issues
```

For more detailed documentation, see [CLAUDE.md](CLAUDE.md).
