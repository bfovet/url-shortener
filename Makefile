run:
	python3 -m url_shortener

check:
	python3 -m ruff check

clean:
	rm -rf build dist src/*.egg-info .tox .pytest_cache pip-wheel-metadata
	find src -name '__pycache__' | xargs rm -rf

install:
	uv pip install -e .

dev:
	uv pip install -e .[dev]
