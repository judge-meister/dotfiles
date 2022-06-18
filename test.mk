# vim: noet

SHELL := bash
MANU := $(shell sudo dmidecode -s system-manufacturer)

######  TESTING RULES  ######
all: test

.PHONY: test
test: shellcheck ## Runs all the tests on the files in the repository.

.PHONY: shellcheck
shellcheck: ## Runs the shellcheck tests on the scripts.
	docker run --rm -i $(DOCKER_FLAGS) \
		--name df-shellcheck \
		-v $(CURDIR):/usr/src:ro \
		--workdir /usr/src \
		jess/shellcheck ./test.sh

.PHONY: pylint_df
pylint_df: ## runs pylint on all the python files in the repo.
	docker run --rm -i $(DOCKER_FLAGS) \
		--name df-pylint \
		-v $(CURDIR):/usr/src:ro \
		--workdir /usr/src \
		judge/pylint ./test_pylint.sh

.PHONY: pylint
pylint: ## runs pylint on all the python files in the repo.
	./test_pylint.sh


# make file for kvm installs
# vim: noet

