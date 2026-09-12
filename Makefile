.PHONY: install generate test docker-build

PYTHON ?= python3

.venv/bin/python:
	$(PYTHON) -c 'import sys; assert sys.version_info >= (3, 10), "Python >= 3.10 is required; set PYTHON=/path/to/python3.12"'
	$(PYTHON) -m venv .venv

install: .venv/bin/python
	.venv/bin/python -m pip install -e '.[dev]'

generate:
	.venv/bin/hilbench generate --overwrite

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/pytest

docker-build:
	docker build -t hil-safety-bench:latest .
