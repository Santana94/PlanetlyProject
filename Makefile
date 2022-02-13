 PROJECT_NAME := PlanetlyProject
PYTHON_VERSION := 3.6.10
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)

code-convention:
	flake8
	pycodestyle

.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	rm -fr staticfiles/

.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/
	rm -f coverage.xml

clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts

setup:
	pip install -r requirements.txt

create-venv:
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down
	rm -rf ./volumes/db

default_target: clean code-convention

test:
	docker-compose run web pytest

docker-migrate:
	docker-compose run web python3 manage.py migrate
