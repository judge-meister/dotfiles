# make file for kvm installs
# vim: noet

SHELL := bash
MANU := $(shell sudo dmidecode -s system-manufacturer)

.PHONY: etc
etc: cleanetc
ifeq ($(MANU), QEMU)
	sudo ln -snfv $(CURDIR)/etc/X11/xorg.conf.d/20-monitor.conf /etc/X11/xorg.conf.d/
endif

.PHONY: cleanetc
cleanetc:
ifeq ($(MANU), QEMU)
	sudo rm -f /etc/X11/xorg.conf.d/20-monitor.conf
endif

