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

SUBLIME_VERSION := $(shell subl --version 2> /dev/null)
UNAME := $(shell uname)

## ============================================================================
##	Basic environment configuration
## ============================================================================
setup:
	@echo Executing development environment setup...
	sudo ./scripts/envinstall
	@echo

## ============================================================================
##	Basic environment configuration
## ============================================================================
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

## ============================================================================
##	Execute semgrep on the codebase with output set to the console
## ============================================================================
semgrep:
	@echo Executing semgrep...
	semgrep --config=p/python ./murasame
	semgrep --config=p/r2c-best-practices ./murasame
	semgrep --config=p/r2c-bug-scan ./murasame
	semgrep --config=p/r2c-ci ./murasame
	semgrep --config=p/r2c-security-audit ./murasame
	@echo

## ============================================================================
##	Execute semgrep on the codebase with output set to SARIF files
## ============================================================================
semgrep-sarif:
	@echo Executing semgrep with SARIF output...
	semgrep --config=p/python -o ${WORKSPACE_DIRECTORY}/logs/semgrep-python.sarif --sarif ./murasame
	semgrep --config=p/r2c-best-practices -o ${WORKSPACE_DIRECTORY}/logs/semgrep-best-practices.sarif --sarif ./murasame
	semgrep --config=p/r2c-bug-scan -o ${WORKSPACE_DIRECTORY}/logs/semgrep-bug-scan.sarif --sarif ./murasame
	semgrep --config=p/r2c-ci -o ${WORKSPACE_DIRECTORY}/logs/semgrep-ci.sarif --sarif ./murasame
	semgrep --config=p/r2c-security-audit -o ${WORKSPACE_DIRECTORY}/logs/semgrep-security-audit.sarif --sarif ./murasame
	@echo

## ============================================================================
##	Installs a version of Murasame on the local machine
## ============================================================================
install: build
	@echo Uninstalling installed library...
	pip uninstall -y murasame
	@echo

	@echo Installing current version...
	pip install $(WORKSPACE_DIRECTORY)/dist/murasame-0.1.0-py3-none-any.whl
	@echo

## ============================================================================
##	Uninstall the installed version of Murasame from the local machine
## ============================================================================
uninstall:
	@echo Uninstalling installed library...
	pip uninstall -y murasame
	@echo

## ============================================================================
##	Builds the Python wheel of the framework
## ============================================================================
build:
	@echo Executing project build...
	./scripts/build --type=development
	@echo

## ============================================================================
##	Builds the documentation of the framework
## ============================================================================
documentation:
	@echo Building project documentation...
	sphinx-build -E -a -b html ./doc/ $(WORKSPACE_DIRECTORY)/dist/documentation/
	@echo

## ============================================================================
##	Executes the unit tests of the framework
## ============================================================================
unittest:
	@echo Executing unit tests...
	pytest -v --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html
	@echo

## ============================================================================
##	Executes the linter on the framework's source code
## ============================================================================
lint:
	@echo Executing linter...
	./scripts/lint.sh
	@echo

## ============================================================================
##	Measures the unit test coverage of the framework
## ============================================================================
coverage:
	@echo Measuring unit test coverage...
	pytest -v --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html --cov=./murasame --cov-report=html --cov-config=./.coveragerc --no-cov-on-fail --cov-fail-under=80
	@echo

## ============================================================================
##	Creates a new PyPi release of the framework
## ============================================================================
release:
	@echo Releasing new version...
	./scripts/build --type=release
	@echo

## ============================================================================
##	Executes SCC in CLI mode
## ============================================================================
loc:
	scc -w .

## ============================================================================
##	Executes SCC with JSON output
## ============================================================================
loc-report:
	scc -f json . > ${WORKSPACE_DIRECTORY}/logs/sccreport.json
	scc -f html . > ${WORKSPACE_DIRECTORY}/logs/sccreport.html

## ============================================================================
##	Creates a dependency graph of current Python dependencies
## ============================================================================
depgraph:
	pydeps --max-bacon=4 --cluster -o ${WORKSPACE_DIRECTORY}/murasame.svg ./murasame

.PHONY: unittest build
