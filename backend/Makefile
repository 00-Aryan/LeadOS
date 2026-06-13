install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

format-check:
	ruff format --check .

lint:
	ruff check .

test:
	PYTHONPATH=. pytest

check: format-check lint test
