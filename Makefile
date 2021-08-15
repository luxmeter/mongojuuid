SHELL := /bin/bash
.PHONY: help

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'

# https://gist.github.com/prwhite/8168133
help: ## Show help
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

clean-pyc:
	@find . -name '.pytest_cache' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f  {} +

clean-build:
	@rm -f -r build/
	@rm -f -r dist/
	@rm -f -r .eggs
	@rm -f -r *.egg-info

clean: clean-pyc clean-build ## Clear all

test: clean-pyc ## Run tests
	@echo ""

build: ## Build project
	@poetry build

install: ## Install project and its dependencies
	@poetry install

publish: build ## Deploy distribution package
	@poetry publish -v -r pypi