## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

SHELL := /bin/bash

WORKSPACE_DIRECTORY =  ~/.murasame
VIRTUALENV_DIRECTORY = ./.env

configure:
	@echo Creating workspace directories...
	mkdir -p $(WORKSPACE_DIRECTORY)
	mkdir -p $(WORKSPACE_DIRECTORY)/build
	mkdir -p $(WORKSPACE_DIRECTORY)/dist
	mkdir -p $(WORKSPACE_DIRECTORY)/testfiles
	mkdir -p $(WORKSPACE_DIRECTORY)/logs
	mkdir -p $(WORKSPACE_DIRECTORY)/logs/unittest
	@echo

	@echo Creating virtual environment in ./.env...
	virtualenv --python=python3.8 $(VIRTUALENV_DIRECTORY)
	@echo

	@echo Installing requirements inside the virtual environment...
	( \
		source $(VIRTUALENV_DIRECTORY)/bin/activate; \
		pip install -r requirements-dev.txt; \
		pip install -r requirements.txt; \
	)
	@echo

install: build
	@echo Uninstalling installed library...
	pip uninstall -y murasame
	@echo

	@echo Installing current version...
	pip install $(WORKSPACE_DIRECTORY)/dist/murasame-0.1.0-py3-none-any.whl
	@echo

uninstall:
	@echo Uninstalling installed library...
	pip uninstall -y murasame
	@echo

build:
	@echo Executing project build...
	./scripts/build --type=development
	@echo

documentation:
	@echo Building project documentation...
	sphinx-build -E -a -b html ./doc/ $(WORKSPACE_DIRECTORY)/dist/documentation/
	@echo

unittest:
	@echo Executing unit tests...
	pytest -v --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html
	@echo

lint:
	@echo Executing linter...
	pylint --rcfile=./.pylintrc --exit-zero ./murasame
	@echo

coverage:
	@echo Measuring unit test coverage...
	pytest -v --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html --cov=./murasame --cov-report=html --cov-config=./.coveragerc --no-cov-on-fail --cov-fail-under=80
	@echo

release:
	@echo Releasing new version...
	./scripts/build --type=release
	@echo

.PHONY: unittest build