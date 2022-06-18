# makefile for sway wm
# vim: noet
SHELL := bash
MANU := $(shell sudo dmidecode -s system-manufacturer)
HOME_CFG=$(HOME)/.config

# ------ common and system ------
common:
	@echo install common files
	ln -snfv $(PWD)/bin $(HOME)/
	ln -snfv $(PWD)/.local/bin $(HOME)/.local/
	ln -snfv $(PWD)/.config/{gtk-3.0,autostart,mpv,tbsm} $(HOME_CFG)/
	ln -snfv $(PWD)/.config/systemd/user $(HOME_CFG)/systemd/
	ln -snfv $(PWD)/{.bashrc,.bash_profile,.bash_aliases,.vimrc,.xinitrc,.xbindkeysrc} $(HOME)/

cleancommon:
	@echo remove common files
	-$(RM) $(HOME)/bin $(HOME)/.local/bin $(HOME_CFG)/{gtk-3.0,autostart,mpv,tbsm}
	-$(RM) $(HOME_CFG)/systemd/user
	-$(RM) $(HOME)/{.bashrc,.bash_profile,.bash_aliases,.vimrc,.xinitrc,.xbindkeysrc} 

distcleancommon:
	@echo remove common files
	-$(RM) -r $(HOME)/bin $(HOME)/.local/bin $(HOME_CFG)/{gtk-3.0,autostart,mpv,tbsm}
	-$(RM) -r $(HOME_CFG)/systemd/user
	-$(RM) $(HOME)/{.bashrc,.bash_profile,.bash_aliases,.vimrc,.xinitrc,.xbindkeysrc} 

.PHONY: etc
etc:
	@echo install system files
	for file in $(shell find etc -type f | grep -v monitor); do \
		sudo mkdir -p /$$(dirname $$file); \
		sudo ln -snfv $(CURDIR)/$$file /$$(dirname $$file)/; \
	done;
ifeq ($(MANU), QEMU)
	sudo ln -snfv $(CURDIR)/etc/X11/xorg.conf.d/20-monitor.conf /etc/X11/xorg.conf.d/
endif

.PHONY: cleanetc
cleanetc: ## remove files installed into etc
	@echo rm etc files
	for file in $(shell find etc -type f); do \
		sudo rm -f /$$file; \
	done;
ifeq ($(MANU), QEMU)
	sudo rm -f /etc/X11/xorg.conf.d/20-monitor.conf
endif

# ------ sway ------

sway: $(HOME_CFG)/sway

$(HOME_CFG)/sway: /usr/bin/sway
	ln -snfv $(PWD)/.config/{sway,waybar,alacritty,dunst} $(HOME_CFG)/

/usr/bin/sway:
	@echo "install dependencies for swaywm"
	sudo pacman -Sy --needed sway swaybg swayidle swaylock waybar alacritty dunst lxsession udiskie wl-clipboard noto-fonts yad
	yay -Sy swaynagmode waynergy nerd-fonts-mononoki clipman

cleansway:
	-$(RM) $(HOME_CFG)/{sway,waybar,alacritty,dunst}

distcleansway:
	-$(RM) -r $(HOME_CFG)/{sway,waybar,alacritty,dunst}

# ------ i3wm ------

i3wm: $(HOME_CFG)/i3

$(HOME_CFG)/i3: /usr/bin/i3
	@echo "install dependencies for i3wm"
	ln -snfv $(PWD)/.config/{i3,i3blocks,alacritty,dunst,picom} $(HOME_CFG)/
	ln -snfv $(PWD)/.fehbg $(HOME)/

/usr/bin/i3:
	@echo sudo pacman -Ss i3
	sudo pacman -Sy --needed i3-gaps i3blocks i3lock i3status alacritty rofi xorg-randr xautolock feh dunst lxsession picom networkmanager volumeicon

cleani3wm:
	-$(RM) $(HOME_CFG)/{i3,i3blocks,alacritty,dunst,picom} $(HOME)/.fehbg

# ------------------------------

distclean: distcleansway \
           distcleancommon

clean: cleansway \
       cleani3wm \
	   cleancommon \
	   cleanetc

all: common \
     etc \
	 sway \
	 i3wm

