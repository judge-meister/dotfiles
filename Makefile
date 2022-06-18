# vim: noet

SHELL := bash
MANU := $(shell sudo dmidecode -s system-manufacturer)

.PHONY: all
all: dotfiles folders etc 

.PHONY: clean
clean: cleandotfiles cleanfolders cleanetc 

.PHONY: dotfiles
dotfiles: cleandotfiles  ## Install the dotfiles
	# add aliases for dotfiles
	for file in $(shell find $(CURDIR) -name ".*" -not -name ".gitignore" -type f); do \
		f=$$(basename $$file); \
		ln -sfnv $$file $(HOME)/$$f; \
	done;

.PHONY: cleandotfiles
cleandotfiles: ## Remove the dotfiles
	for file in $(shell find $(CURDIR) -name ".*" -not -name ".gitignore" -type f); do \
		f=$$(basename $$file); \
		rm -fv $(HOME)/$$f; \
	done;

.PHONY: folders
folders: cleanfolders ## do lower directories
	for file in $(shell find .config .local bin docs dockerfiles -type f | grep -v -E 'wofi|__pycache__' ); do \
		d=$$(dirname $$file); \
		mkdir -p $(HOME)/$$d; \
		ln -snfv $(CURDIR)/$$file $(HOME)/$$d/ ; \
	done; \
	systemctl --user daemon-reload;

.PHONY: cleanfolders
cleanfolders: ## do lower directories
	for file in $(shell find .config .local bin docs dockerfiles -type f ); do \
		f=$$(basename $$file); \
		rm -fv $(HOME)/$$file ; \
	done;

.PHONY: Pictures
Pictures: cleanPictures ## do Pictures folder
	for file in $(shell find Pictures -maxdepth 1 -mindepth 1); do \
		f=$$(basename $$file); \
		mkdir -p $(HOME)/Pictures; \
		ln -snfv $(CURDIR)/$$file $(HOME)/Pictures/; \
	done;

.PHONY: cleanPictures
cleanPictures: ## 
	rm -frv $(HOME)/Pictures/;

.PHONY: etc
etc: cleanetc ## install etc files
	for file in $(shell find etc -type f | grep -v monitor); do \
		sudo mkdir -p /$$(dirname $$file); \
		sudo ln -snfv $(CURDIR)/$$file /$$(dirname $$file)/; \
	done;
ifeq ($(MANU), QEMU)
	sudo ln -snfv $(CURDIR)/etc/X11/xorg.conf.d/20-monitor.conf /etc/X11/xorg.conf.d/
endif

.PHONY: cleanetc
cleanetc: ## remove files installed into etc
	for file in $(shell find etc -type f); do \
		sudo rm -f /$$file; \
	done;
ifeq ($(MANU), QEMU)
	sudo rm -f /etc/X11/xorg.conf.d/20-monitor.conf
endif

######  TESTING RULES  ######

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

