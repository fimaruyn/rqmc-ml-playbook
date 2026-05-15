.PHONY: build shell run pdf pdf-clean test help

IMAGE := rqmc-ml-playbook:latest
VOLUME_MOUNT := -v "$(CURDIR):/app"
DOCKER_RUN := docker run --rm $(VOLUME_MOUNT) $(IMAGE)

help:
	@echo 'Available targets:'
	@echo '  build        - Build Docker image'
	@echo '  shell        - Interactive bash session'
	@echo '  run ARGS=... - Run arbitrary command'
	@echo '  pdf          - Compile theory/main.tex to PDF (XeLaTeX)'
	@echo '  pdf-clean    - Remove LaTeX artifacts'
	@echo '  test         - Run pytest suite'

build:
	docker build -t $(IMAGE) .

shell:
	$(DOCKER_RUN) -it /bin/bash

run:
	$(DOCKER_RUN) $(ARGS)

pdf:
	$(DOCKER_RUN) "cd theory && latexmk -xelatex -interaction=nonstopmode main.tex"

pdf-clean:
	$(DOCKER_RUN) "cd theory && latexmk -c"

test:
	$(DOCKER_RUN) "python -m pytest tests/ -v"

##@ CI/CD Helpers

ci-lint:
	_uv pip install --system -e ".[dev]"
	_ruff check src/ tests/ scripts/
	_mypy src/ scripts/

ci-test:
	_uv pip install --system -e ".[dev]"
	_pytest tests/ -v --cov=src

ci-docker:
	_docker build -t $(IMAGE):ci-test .
	_docker run --rm $(IMAGE):ci-test -c "import salib, numpy, scipy; print('Imports OK')"
	_docker run --rm -v "$(CURDIR):/app" $(IMAGE):ci-test -m pytest tests/ -v

ci-all: ci-lint ci-test ci-docker