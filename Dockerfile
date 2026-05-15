# syntax=docker/dockerfile:1.4
# rqmc-ml-playbook/Dockerfile
# Reproducible environment for RQMC research with Russian LaTeX support

FROM python:3.12-slim-bookworm AS base

# ========== METADATA ==========
LABEL org.opencontainers.image.title="RQMC-ML Playbook"
LABEL org.opencontainers.image.description="Reproducible research environment for Randomized Quasi-Monte Carlo methods in ML with Russian LaTeX support"
LABEL org.opencontainers.image.authors="Vladimir Belov <vladimir.belov.an@gmail.com>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/fimaruyn/rqmc-ml-playbook"

# ========== ENVIRONMENT ==========
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # LaTeX: use XeLaTeX as default engine for polyglossia support
    LATEXMK_ENGINE=xelatex

# ========== SYSTEM DEPENDENCIES ==========
# System dependencies: build tools + LaTeX + fonts + fontconfig
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials for Python packages
    build-essential git curl ca-certificates \
    libopenblas-dev liblapack-dev \
    # XeLaTeX engine and core packages
    texlive-xetex \
    texlive-lang-cyrillic \
    texlive-lang-english \
    # Font support and fontconfig (REQUIRED for fc-cache)
    texlive-fonts-recommended \
    fonts-liberation \
    fonts-linuxlibertine \
    fontconfig \
    # Additional LaTeX packages for mathematics and bibliography
    texlive-latex-extra \
    texlive-science \
    texlive-bibtex-extra \
    biber \
    latexmk \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* && apt-get clean \
    # Update font cache (now fontconfig is installed)
    && fc-cache -fv

# ========== PYTHON TOOLCHAIN ==========
# Install uv via pip (more reliable than ghcr.io in restricted networks)
RUN pip install --no-cache-dir "uv>=0.4.0,<0.6.0"

# ========== WORKSPACE SETUP ==========
WORKDIR /app

# Copy ALL source files BEFORE installing Python dependencies
# This ensures pyproject.toml, README.md, src/, theory/ are all present
COPY . .

# ========== PYTHON DEPENDENCIES ==========
# Install core scientific stack explicitly first (ensures SALib is installed)
RUN uv pip install --system --no-cache \
    "numpy>=1.24.0" "scipy>=1.12.0" "SALib>=1.4.0" \
    "pyyaml>=6.0" "loguru>=0.7.0" "matplotlib>=3.7.0" "pandas>=2.0.0" && \
    # Then install dev dependencies
    uv pip install --system --no-cache ".[dev]"

# ========== NON-ROOT USER ==========
# Create non-root user for security best practice
RUN useradd -m -u 1000 researcher && \
    chown -R researcher:researcher /app && \
    chmod -R 755 /app
USER researcher

# ========== ENTRYPOINT ==========
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python"]