FROM ubuntu:24.04
ENV MODE dev
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_BREAK_SYSTEM_PACKAGES=1


RUN apt-get update \
    && apt-get install --no-install-recommends -yq \
      build-essential \
      python3 \
      python3-dev \
      make \
      netcat-openbsd \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Copy uv from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Use copy instead of hardlink (cache and target are on different filesystems)
ENV UV_LINK_MODE=copy

# Copy only dependency files first (for better Docker layer caching)
COPY pyproject.toml uv.lock ./
# Install Python dependencies in a virtual environment
RUN uv sync --frozen --no-dev --no-cache --compile-bytecode
