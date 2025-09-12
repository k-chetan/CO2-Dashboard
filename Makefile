.PHONY: setup install format test run-pipeline run-app

setup:
	python3 -m venv .venv
	@echo "Virtual environment created. Activate it with: source .venv/bin/activate"

install:
	pip install -r requirements.txt -r requirements_dev.txt

format:
	black .
	isort .

test:
	pytest

run-pipeline:
	python src/ingest.py
	python src/transform.py
	python src/load.py

run-app:
	streamlit run app.py
