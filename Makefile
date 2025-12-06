.PHONY: setup install format test run-pipeline run-app

setup:
	python3 -m venv .venv
	@echo "Virtual environment created. Activate it with: source .venv/bin/activate"

install:
	pip install -r requirements.txt -r requirements_dev.txt
	pip install pytest

format:
	black .
	isort .

test:
	python -m pytest src/tests -v

run-pipeline:
	python src/ingest.py
	python src/transform.py
	python src/load.py

run-app:
	streamlit run app.py

docker-build:
	docker-compose build

docker-pipeline:
	# Run ingest and transform INSIDE the container
	docker-compose run --rm --entrypoint "python src/ingest.py" co2-app
	docker-compose run --rm --entrypoint "python src/transform.py" co2-app

docker-run:
	docker-compose up
