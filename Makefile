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
