.PHONY: build shell run test clean

IMAGE := rqmc-ml-playbook:latest
VOLUME_MOUNT := -v "$(CURDIR):/app"
DOCKER_RUN := docker run --rm $(VOLUME_MOUNT) $(IMAGE)

build:
	docker build -t $(IMAGE) .

shell:
	$(DOCKER_RUN) -it /bin/bash

run:
	$(DOCKER_RUN) $(ARGS)

test:
	$(DOCKER_RUN) -m pytest tests/ -v

clean:
	docker rmi $(IMAGE) 2>$null || true
	docker image prune -f
