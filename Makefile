.PHONY: quality style

DOCKER_FILE=docker/Dockerfile
PYTHON_VERSION?=3.7
SRC?=$(shell 'pwd')

check_dirs := encoded_video examples

help:
	@cat Makefile

build:
	docker build -t encoded-video --build-arg python_version=$(PYTHON_VERSION) -f $(DOCKER_FILE) .
bash: build
	docker run --rm -it -v $(SRC):/src/workspace encoded-video bash

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black $(check_dirs)
	isort $(check_dirs)

test:
	pytest -sv tests/

