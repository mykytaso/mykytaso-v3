# ==========================================
# STAGE 1: Builder
# ==========================================
# Use Python 3.13 slim image as builder stage to install dependencies
# This stage is temporary and won't be in the final image (saves space)
FROM python:3.13-slim AS builder

# Set working directory for the builder stage
WORKDIR /app

# Copy uv from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only dependency files first (for better Docker layer caching)
# If these files don't change, Docker can reuse this layer
COPY pyproject.toml uv.lock ./

# Install Python dependencies in a virtual environment
# --frozen: Use exact versions from uv.lock (reproducible builds)
# --no-dev: Don't install development dependencies (smaller image)
# --no-cache: Don't cache packages (saves space)
# --compile-bytecode: Pre-compile Python files for faster startup
RUN uv sync --frozen --no-dev --no-cache --compile-bytecode


# ==========================================
# STAGE 2: Final Runtime Image
# ==========================================
# Start fresh with a clean Python 3.13 slim image
# This creates a smaller final image without build artifacts
FROM python:3.13-slim

# Set working directory for the application
WORKDIR /app

# Install runtime system dependencies
# libpq5: PostgreSQL client library (required for psycopg2)
# netcat-openbsd: Network utility for health checks (checking if database is ready)
# --no-install-recommends: Install only essential packages (smaller image)
# rm -rf /var/lib/apt/lists/*: Clean up apt cache (saves ~40MB)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy uv tool again (needed in final image to run the app)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the virtual environment from builder stage
# This contains all installed Python packages
COPY --from=builder /app/.venv /app/.venv

# Copy dependency files (needed for uv to work correctly)
COPY pyproject.toml uv.lock ./

# Copy all Django project files and directories
# These are the actual source code files
COPY manage.py ./
COPY app ./app
COPY users ./users
COPY posts ./posts
COPY utils ./utils
COPY frontend ./frontend

# Create a non-root user for security
# Running as root in containers is a security risk
# -m: Create home directory
# -u 1000: Set user ID to 1000 (standard for first user)
# Then change ownership of all app files to this user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user for running the application
USER appuser

# Set environment variables
# PATH: Add virtual environment binaries to PATH so Python can find them
# PYTHONPATH: Add /app to Python's module search path
# PYTHONUNBUFFERED: Force Python output to be sent directly (better for logs)
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files (cleaner container)
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port 8000 (Django's default port)
# This is documentation - actual port mapping happens in docker-compose.yml
EXPOSE 8000

# Default command to run when container starts
# uv run: Use uv to run the command in the virtual environment
# manage.py runserver: Start Django development server
# 0.0.0.0:8000: Bind to all interfaces (allows external connections to container)
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
