# Personal Blog Platform

A production-ready blog application showcasing modern Django development practices, PostgreSQL database design, and full-stack engineering capabilities.

## Technical Stack

### Core Technologies
- **Python 3.12+** - Leveraging modern Python features and type hints
- **Django 6.0+** - Latest Django framework with async support
- **PostgreSQL** - Relational database with advanced indexing strategies
- **uv** - Modern Python package manager for fast dependency resolution

### Production Infrastructure
- **Gunicorn + Uvicorn Workers** - ASGI server with async worker support
- **Docker + Docker Compose** - Containerized development and deployment
- **Nginx** - Reverse proxy configuration for production
- **Sentry** - Real-time error tracking and performance monitoring

### Frontend & Content Rendering
- **markdown-it-py 4.x** - CommonMark parsing with custom renderer implementation
- **Pygments** - Syntax highlighting with configurable themes
- **Django Templates** - Server-side rendering with context processors

## Architecture Highlights

### Single-Author Design
This is a personal blog with one author. There is no public sign-up:
- Content is managed entirely through Django admin
- Custom `User` model with email-based login and a custom manager (`UserAccountManager`)
- Readers browse and like posts without any account

### Advanced Blog Post Management
- **Dual rendering modes**: Markdown with custom renderer or raw HTML
- **HTML caching strategy**: Cached markdown rendering with selective cache invalidation
- **Slug generation**: Automatic URL-friendly slug creation with uniqueness guarantees
- **Visibility controls**: Published/draft states with timezone-aware publishing
- **OpenGraph metadata**: SEO-optimized with custom OG tags per post
- **View counting**: Non-intrusive pageview tracking

### Like System
Account-free like system tracked entirely by IP address:
- Database constraint ensuring one like per IP per post
- Composite index on `[post, ip_address]` for query optimization
- IP extraction handling `X-Forwarded-For` headers for proxied requests

### Custom Markdown Renderer
Built a custom markdown-it-py renderer with Pygments integration:
- Syntax highlighting on fenced and indented code blocks
- Image rendering with figure/figcaption elements
- Support for tables and strikethrough
- Automatic heading anchors, so sections can be deep-linked
- Configurable code highlighting themes

## Engineering Practices

### Code Quality & Linting
Comprehensive Ruff configuration with 40+ rule sets enabled:
- `pycodestyle`, `pyflakes`, `isort` for code style and import sorting
- `flake8-django` for Django-specific best practices
- `flake8-bandit` for security vulnerability detection
- `flake8-bugbear` for detecting likely bugs
- `flake8-simplify` and `flake8-comprehensions` for code optimization
- `pylint` for additional static analysis
- Maximum cyclomatic complexity of 10
- Google-style docstring convention

### Database Design
- UUID primary keys for posts (security and scalability)
- Composite indexes for optimized query performance
- Foreign key relationships with proper `on_delete` behaviors
- Soft delete pattern maintaining referential integrity
- Timezone-aware datetime fields throughout

### Security Implementations
- No public sign-up: admin login is the only authenticated entry point
- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS protection with proper template escaping
- Secure password hashing with Django's PBKDF2 algorithm
- Environment-based secret management (no hardcoded credentials)

### Development Workflow
- Makefile with common development commands (documented in `README_MAKEFILE.md`)
- Docker Compose for local development environment
- Separate production Docker configuration
- Database migrations version controlled
- Static file cache busting with dynamic hashing
- Request logging middleware for debugging

### Containerized Database
PostgreSQL runs in Docker in **both** development and production, so the database version is pinned in the repository rather than depending on what happens to be installed on the host:

- `postgres:18.0` in both compose files
- Data persisted in a named volume (`db-data`), surviving container recreation
- Health check gating: the app container starts only once Postgres reports ready
- In production the database port is published on `127.0.0.1` only — never exposed to the internet
- Credentials defined once via a YAML anchor and shared between the app and database services
- Backup and restore through `make prod-db-backup` / `make prod-db-restore`, with a nightly cron job and 14-day retention

The production host keeps no PostgreSQL client of its own. Every database operation runs inside the container, so the client and server versions can never drift apart. The host needs only Docker and `make` (`sudo apt install make`) — the deploy workflow copies the `Makefile` alongside the compose file.

### CI/CD Pipeline
Automated deployment using GitHub Actions with two-stage pipeline:

**Build Stage:**
- Triggered on push to `main` branch
- Builds Docker image with multi-tagging strategy (`latest` + commit SHA)
- Pushes to GitHub Container Registry (ghcr.io)
- Ensures reproducible builds with SHA-based versioning

**Deploy Stage:**
- Generates environment file from GitHub Secrets
- Securely transfers configuration via SSH with key-based authentication
- Deploys docker-compose.production.yaml to remote server
- Pulls the SHA-versioned image and recreates the app container
- Cleans up superseded images from previous deployments
- The database container is left running and is not recreated by a deploy

**Security & Configuration Management:**
- All sensitive data managed through GitHub Secrets
- SSH key authentication for secure remote deployment
- Environment variables include: Django settings, PostgreSQL credentials, Sentry DSN
- Git commit SHA injected for static asset cache busting
- Separation of development and production compose configurations

## Key Features

### Content Management
- Markdown-based post creation with live preview capability
- Rich text editing with syntax highlighting support
- Draft/publish workflow with scheduled publishing
- Post visibility controls (public/private)
- Automatic sitemap generation for SEO

### Reader Engagement
- Like functionality for posts
- Anonymous interaction tracking (no account needed)

### Developer Experience
- Clean separation of concerns (apps: `users`, `posts`, `likes`, `markdown`, `utils`)
- Reusable utility modules for common operations
- Custom template tags for complex rendering logic
- Context processors for global template variables
- Comprehensive middleware pipeline

---

This project demonstrates proficiency in:
- Modern Python and Django development patterns
- PostgreSQL database design and optimization
- CI/CD pipeline implementation with GitHub Actions
- Production-ready deployment configuration
- Security best practices and vulnerability prevention
- Clean architecture and separation of concerns
- Custom user model design
- Performance optimization (caching, indexing, query optimization)
- Third-party API integration (Sentry)
- Docker containerization and orchestration
- DevOps practices (SSH automation, secret management, zero-downtime deployments)
- Code quality tooling and static analysis.