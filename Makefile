
.PHONY: build down up test

build:
	docker compose build --no-cache

down:
	docker compose down --volumes --rmi local

up: down build
	docker compose up

black:
	black .
