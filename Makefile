# Makefile for Homematic(IP) Local for OpenCCU
#
# All targets run through script/run-in-env.sh, which activates ./venv (or .venv)
# if present, so they work with or without an activated virtual environment.
#
# Run `make` or `make help` for an overview of all targets.

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# --- Configuration -----------------------------------------------------------

PYTHON ?= python3.14
VENV ?= venv
RUN := script/run-in-env.sh
PKG := custom_components/homematicip_local
TESTS := tests
CONFIG_DIR ?= config

# Extra args, e.g. `make test PYTEST_ARGS="-x -vv"` or `make test-file FILE=tests/test_init.py`
PYTEST_ARGS ?=
FILE ?=

# Docker images used by the HA/HACS validation targets
HASSFEST_IMAGE := ghcr.io/home-assistant/hassfest:latest
HACS_IMAGE := ghcr.io/hacs/action:main

.PHONY: help venv bootstrap setup install hooks upgrade-deps \
        format format-check lint mypy pylint bandit codespell yamllint prettier \
        sort-class-members translations translations-fix flow-translations \
        prek prek-manual \
        test test-fast test-cov test-cov-html test-file test-e2e test-ci \
        hassfest hacs validate \
        hass check ci version clean clean-all

# --- Help --------------------------------------------------------------------

help: ## Show this help
	@echo ""
	@echo "Homematic(IP) Local for OpenCCU - development targets"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5); next } \
		/^[a-zA-Z0-9_-]+:.*?## / { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

##@ Setup

venv: ## Create the virtual environment (./venv, Python 3.14)
	$(PYTHON) -m venv $(VENV)
	@echo "Created $(VENV). Next: make setup"

bootstrap: ## Install development and test dependencies
	script/bootstrap

setup: ## Full setup: dependencies + git hooks
	script/setup

install: ## (Re-)install requirements_test.txt via uv
	$(RUN) uv pip install --prerelease=allow -r requirements_test.txt

hooks: ## Install the prek/pre-commit git hooks
	$(RUN) prek install

upgrade-deps: ## Update pinned versions in the requirements files (pur)
	$(RUN) pur -r requirements_test_pre_commit.txt
	$(RUN) pur -r requirements_test.txt

##@ Code quality

format: ## Format and auto-fix code (ruff format + ruff check --fix)
	$(RUN) ruff format $(PKG) $(TESTS) script
	$(RUN) ruff check --fix $(PKG) $(TESTS) script

format-check: ## Check formatting without writing changes
	$(RUN) ruff format --check $(PKG) $(TESTS) script

lint: ## Lint with ruff (no auto-fix)
	$(RUN) ruff check $(PKG) $(TESTS) script

mypy: ## Type check (strict mode)
	$(RUN) mypy $(PKG)

pylint: ## Lint with pylint
	$(RUN) pylint -j 0 $(PKG)

bandit: ## Security lint
	$(RUN) bandit --quiet --configfile tests/bandit.yaml -r $(PKG) script

# Only git-tracked files: a locally installed HACS lives under custom_components/hacs.
codespell: ## Spell check
	$(RUN) codespell --ignore-words-list=hass --quiet-level=2 $$(git ls-files \
		| grep -vE '\.(csv|json)$$|^tests/fixtures/|^$(PKG)/frontend/|^\.github/ISSUE_TEMPLATE/bug_report_de\.yml$$')

yamllint: ## Lint YAML files
	$(RUN) yamllint $$(git ls-files '*.yaml' '*.yml')

prettier: ## Format Markdown/YAML/JSON with prettier (requires npx)
	npx --yes prettier --write .

sort-class-members: ## Enforce class member ordering
	$(RUN) python script/sort_class_members.py $$(git ls-files '$(PKG)' '$(TESTS)' | grep '\.py$$')

translations: ## Validate strings.json / en.json / de.json
	$(RUN) python script/check_translations.py

translations-fix: ## Sort and sync the translation files
	$(RUN) python script/check_translations.py --fix

flow-translations: ## Validate config flow & repair translations
	$(RUN) python script/check_flow_translations.py

prek: ## Run all prek hooks (the full quality gate)
	$(RUN) prek run --all-files

prek-manual: ## Run manual-stage hooks (python-typing-update, ...)
	$(RUN) prek run --hook-stage manual --all-files

##@ Tests

test: ## Run the test suite
	$(RUN) pytest $(TESTS) $(PYTEST_ARGS)

test-fast: ## Run the test suite without slow tests
	$(RUN) pytest $(TESTS) -m "not slow" $(PYTEST_ARGS)

test-cov: ## Run tests with coverage report
	$(RUN) pytest --cov=custom_components $(TESTS) $(PYTEST_ARGS)

test-cov-html: ## Run tests with HTML coverage report (htmlcov/index.html)
	$(RUN) pytest --cov=custom_components --cov-report=html $(TESTS) $(PYTEST_ARGS)
	@echo "Report: htmlcov/index.html"

test-file: ## Run a single test file: make test-file FILE=tests/test_init.py
	@test -n "$(FILE)" || { echo "Usage: make test-file FILE=tests/test_init.py"; exit 1; }
	$(RUN) pytest $(FILE) $(PYTEST_ARGS)

test-e2e: ## Run the opt-in three-way parity e2e tests (needs godevccu, openccu-loom, mosquitto)
	$(RUN) pytest $(TESTS)/e2e -m e2e -n0 -s $(PYTEST_ARGS)

test-ci: ## Run tests exactly like the CI pipeline
	$(RUN) pytest --cov=custom_components $(TESTS) --asyncio-mode=legacy $(PYTEST_ARGS)

##@ Validation

hassfest: ## Validate the manifest with hassfest (requires Docker)
	docker run --rm -v "$(CURDIR):/github/workspace" $(HASSFEST_IMAGE)

hacs: ## Validate the repository with the HACS action (requires Docker)
	docker run --rm -v "$(CURDIR):/github/workspace" \
		-e INPUT_CATEGORY=integration -e GITHUB_REPOSITORY=SukramJ/homematicip_local \
		$(HACS_IMAGE)

validate: hassfest hacs ## Run hassfest and HACS validation

##@ Run

hass: ## Start Home Assistant against the local ./config directory
	$(RUN) hass -c $(CONFIG_DIR) --debug

version: ## Show the integration version from manifest.json
	@$(RUN) python -c "import json,pathlib;print(json.loads(pathlib.Path('$(PKG)/manifest.json').read_text())['version'])"

##@ Meta

check: prek test-cov ## Full quality gate: all hooks + tests with coverage

ci: format-check lint mypy pylint test-ci ## Reproduce the CI checks locally

##@ Housekeeping

clean: ## Remove caches, coverage data and build artifacts
	rm -rf .mypy_cache .ruff_cache .pytest_cache htmlcov .coverage .coverage.*
	find . -path ./venv -prune -o -type d -name __pycache__ -print0 | xargs -0 rm -rf
	find . -path ./venv -prune -o -type d -name "*.egg-info" -print0 | xargs -0 rm -rf

clean-all: clean ## Also remove the virtual environment
	rm -rf $(VENV)
