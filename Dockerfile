# Official uv image: Debian 13 (trixie) slim with Python 3.12 and uv preinstalled.
# Pinned uv version for reproducible builds.
FROM ghcr.io/astral-sh/uv:0.11.31-python3.12-trixie

ENV MODE=dev
ENV DEBIAN_FRONTEND=noninteractive
# Copy instead of hardlink (cache and target are on different filesystems).
ENV UV_LINK_MODE=copy

# Runtime system packages only:
#   make            -> production starts with `make prod`
#   netcat-openbsd  -> dev compose waits for the db with `nc -z db 5432`
#   ca-certificates -> HTTPS calls (Mailgun API via requests)
RUN apt-get update \
    && apt-get install --no-install-recommends -yq \
      make \
      netcat-openbsd \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first so this layer is cached unless pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache --compile-bytecode

# Then copy the application code.
COPY . /app