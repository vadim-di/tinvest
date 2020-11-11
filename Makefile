.DEFAULT_GOAL := help
CODE = tinvest tests
TEST = pytest $(args) --verbosity=2 --showlocals --strict --log-level=DEBUG

.PHONY: help
help:
	@echo 'Usage: make [target] ...'
	@echo ''
	@echo '    make all'
	@echo '    make format'
	@echo '    make lint'
	@echo '    make test'
	@echo '    make test-report'
	@echo '    make mut'
	@echo '    make build'
	@echo '    make docs'
	@echo '    make clean'
	@echo ''

.PHONY: all
all: format lint test test-report build docs clean

.PHONY: update
update:
	poetry update

.PHONY: test
test:
	$(TEST) --cov

.PHONY: test-report
test-report:
	$(TEST) --cov --cov-report html
	python -m webbrowser 'htmlcov/index.html'

.PHONY: lint
lint:
	flake8 --jobs 1 --statistics --show-source $(CODE)
	pylint --jobs 1 --rcfile=setup.cfg $(CODE)
	black --skip-string-normalization --line-length=88 --check $(CODE)
	pytest --dead-fixtures --dup-fixtures
	mypy $(CODE)
	# ignore pipenv for travis-ci
	safety check --full-report --ignore=38334

.PHONY: format
format:
	autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	isort $(CODE)
	black --skip-string-normalization --line-length=88 $(CODE)
	unify --in-place --recursive $(CODE)

.PHONY: docs
docs:
	typer tinvest.cli.app utils docs --name tinvest > docs/cli.md
	mkdocs build -s -v

.PHONY: docs
docs-serve:
	mkdocs serve

.PHONY: build
build:
	poetry build

.PHONY: clean
clean:
	rm -rf docs/cli.md || true
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true

.PHONY: mut
mut:
	mutmut run
