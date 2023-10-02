cheers:
	@echo "Na zdraví! 🍺"

dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

stop:
	@docker compose -f docker-compose.yaml down

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

tests: run
	@docker exec -it postgres-seed poetry run pytest

build:
	@poetry shell
	@poetry run black .
	@poetry run isort . --profile black
	@poetry run pylint **/*.py