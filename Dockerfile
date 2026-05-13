# syntax=docker/dockerfile:1.4
# rqmc-ml-playbook/Dockerfile
# FIX: Handle SALib case-sensitivity on Linux filesystem

FROM python:3.12-slim-bookworm AS base

LABEL org.opencontainers.image.title="RQMC-ML Playbook"
LABEL org.opencontainers.image.authors="Vladimir Belov <vladimir.belov.an@gmail.com>"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl ca-certificates \
    libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Install uv via pip
RUN pip install --no-cache-dir "uv>=0.4.0,<0.6.0"

WORKDIR /app

# Copy all source files BEFORE installing
COPY . .

# Install dependencies explicitly
RUN uv pip install --system --no-cache \
    "numpy>=1.24.0" "scipy>=1.12.0" "SALib>=1.4.0" \
    "pyyaml>=6.0" "loguru>=0.7.0" "matplotlib>=3.7.0" "pandas>=2.0.0" && \
    uv pip install --system --no-cache ".[dev]"

# ✅ FIX: Create lowercase symlink for SALib if needed (Linux case-sensitivity)
# FIX: Create lowercase symlink for SALib if needed (Linux case-sensitivity)
RUN python -c "import sys; from pathlib import Path; sp=Path(sys.prefix)/'lib/python3.12/site-packages'; su=sp/'SALib'; sl=sp/'salib'; \
    (sl.symlink_to(su) and print(f'✅ Created symlink: {sl} -> {su}')) if su.exists() and not sl.exists() and not sl.is_symlink() else print('✅ SALib import path already correct')"
# Non-root user
RUN useradd -m -u 1000 researcher && \
    chown -R researcher:researcher /app && \
    chmod -R 755 /app
USER researcher

# Explicit Python entrypoint
ENTRYPOINT ["/usr/local/bin/python"]
CMD []