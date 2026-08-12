.PHONY: install test lint format migrate run docker

install:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install || true

test:
	pytest -q

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .
	ruff check --fix .

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app --reload --port 8000

docker:
	docker compose up --build
