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
- **Mistune 3.x** - Markdown parsing with custom renderer implementation
- **Pygments** - Syntax highlighting with configurable themes
- **Django Templates** - Server-side rendering with context processors

## Architecture Highlights

### Custom Authentication System
Implemented a custom `User` model with email-based authentication, replacing Django's default username-based system:
- Email verification with expiring tokens
- Soft delete functionality (preserves data integrity)
- Pending email change verification flow
- Custom user manager (`UserAccountManager`)

### Advanced Blog Post Management
- **Dual rendering modes**: Markdown with custom renderer or raw HTML
- **HTML caching strategy**: Cached markdown rendering with selective cache invalidation
- **Slug generation**: Automatic URL-friendly slug creation with uniqueness guarantees
- **Visibility controls**: Published/draft states with timezone-aware publishing
- **OpenGraph metadata**: SEO-optimized with custom OG tags per post
- **View counting**: Non-intrusive pageview tracking

### Sophisticated Like System
Engineered a like system supporting both authenticated and anonymous users:
- Authenticated users tracked via foreign key relationships
- Anonymous users tracked via IP address extraction
- Database constraints ensuring one like per user/IP per post
- Composite indexes on `[post, user]` and `[post, ip_address]` for query optimization
- IP extraction handling `X-Forwarded-For` headers for proxied requests

### Custom Markdown Renderer
Built a custom Mistune renderer with Pygments integration:
- Syntax highlighting with line numbers
- Custom heading anchor generation
- Image rendering with figure/figcaption elements
- Support for tables, strikethrough, and URL auto-linking
- Configurable code highlighting themes

### Email Infrastructure
Implemented transactional email system using Mailgun API:
- Direct API integration (not Django's email backend)
- HTML and plain text template pairs
- Email verification and password reset flows
- Environment-based configuration for development/production

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
- ReCAPTCHA integration for spam prevention
- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS protection with proper template escaping
- Secure password hashing with Django's PBKDF2 algorithm
- Environment-based secret management (no hardcoded credentials)

### Development Workflow
- Makefile with common development commands
- Docker Compose for local development environment
- Separate production Docker configuration
- Database migrations version controlled
- Static file cache busting with dynamic hashing
- Request logging middleware for debugging

### CI/CD Pipeline
Automated deployment using GitHub Actions with two-stage pipeline:

**Build Stage:**
- Triggered on push to `main` branch
- Builds Docker image with multi-tagging strategy (`latest` + commit SHA)
- Pushes to GitHub Container Registry (ghcr.io)
- Ensures reproducible builds with SHA-based versioning

**Deploy Stage:**
- Generates environment file from GitHub Secrets (14+ secret variables)
- Securely transfers configuration via SSH with key-based authentication
- Deploys docker-compose.production.yaml to remote server
- Pulls versioned Docker image and performs zero-downtime restart
- Automatic cleanup of unused images with `docker system prune`

**Security & Configuration Management:**
- All sensitive data managed through GitHub Secrets
- SSH key authentication for secure remote deployment
- Environment variables include: Django settings, PostgreSQL credentials, Mailgun API keys, Sentry DSN, ReCAPTCHA keys
- Git commit SHA injected for static asset cache busting
- Separation of development and production compose configurations

## Key Features

### Content Management
- Markdown-based post creation with live preview capability
- Rich text editing with syntax highlighting support
- Draft/publish workflow with scheduled publishing
- Post visibility controls (public/private)
- Automatic sitemap generation for SEO

### User Engagement
- Like functionality for posts
- Anonymous interaction tracking
- User profile management
- Email preference management

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
- Custom authentication and authorization flows
- Performance optimization (caching, indexing, query optimization)
- Third-party API integration (Mailgun, Sentry, ReCAPTCHA)
- Docker containerization and orchestration
- DevOps practices (SSH automation, secret management, zero-downtime deployments)
- Code quality tooling and static analysis.