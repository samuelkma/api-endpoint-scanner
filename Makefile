.PHONY: test lint run

test:
	poetry run pytest -q

lint:
	poetry run black . && poetry run isort . && poetry run flake8

run:
	poetry run python -m scanner.cli http://127.0.0.1:8000