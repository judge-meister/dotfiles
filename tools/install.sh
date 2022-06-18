#!/bin/bash
set -o pipefail

#
# script to install all dependent packages
#

# change pacman settings
# update sudo to make current user an admin
# install packages via pacman
# install yay
# install some AUR packages
# install my version of dwm and dwmblocks along with distrotube's st and dmenu


# -----------------------------------------------------------------------------
# adjust pacman settings
pacman_settings()
{
  echo "Adjust some pacman settings"; sleep 2

  [ ! -f /etc/pacman.conf.bak ] && sudo cp /etc/pacman.conf /etc/pacman.conf.bak

  sudo sed -e 's/\(ParallelDownloads = .*$\)/\1\nILoveCandy/g' \
      -e 's/^#Color$/Color/' \
      -e 's/^#ParallelDownloads = /ParallelDownloads = /' \
      -e 's/^ILoveCandy//g' \
      -i /etc/pacman.conf
}

# -----------------------------------------------------------------------------
# add sudoers file for current user
make_user_admin()
{
    if [ "$USER" != "root" ]
    then
        echo "This option should be run as root user. Use su to change to root first."
        exit 1
    fi
    echo "Type username to add to sudoers config:"
    # shellcheck disable=SC2162
    read admin
    echo "$admin ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/"$admin"
    chmod 600 /usr/sudoers.d/"$admin"
}

# -----------------------------------------------------------------------------
# script to install yay
install_yay_from_git()
{
  echo "Installing yay from git"; sleep 2

  cd /opt || exit
  sudo git clone https://aur.archlinux.org/yay.git
  sudo chown -R judge:judge /opt/yay
  cd yay || exit
  makepkg -si
}

# -----------------------------------------------------------------------------
# AUR
install_aur_packages()
{
  echo "Installing Required AUR Packages"; sleep 2

  # bare minimum
  yay -Sy --needed \
    i3lock-fancy-git \
    icdiff \
    swaynagmode \
    tbsm \
    ttf-ms-fonts \
    nerd-fonts-mononoki \

  # extras
  yay -Sy --needed \
    brave-bin \
    fontviewer \
    libxft-bgra-git \
    play-with-mpv-git \
    rofi-lbonn-wayland-git \
    tabbed \
    tulizu \
    wev \
    xbindkeys_config-gtk2 

  PRODUCT=$(cat /sys/class/dmi/id/product_name)
  if [ "$PRODUCT" == "MacBookPro5,5" ]
  then
    yay -Sy --needed \
      b43-firmware \
      refind-git
  fi
}

# -----------------------------------------------------------------------------
# packages to install
install_pacman_packages()
{
  echo "Installing Required Packages"; sleep 2
  # xorg group and bits
  sudo pacman -Sy --needed \
    xorg \
    xorg-xinit \
    xclip \
    xorg-xclipboard \

  # wm / de
  sudo pacman -Sy --needed \
    acpi \
    adobe-source-sans-fonts \
    awesome \
    dunst \
    i3-gaps \
    i3blocks \
    lxsession \
    pamixer \
    pavucontrol \
    picom \
    python-iwlib \
    python-psutil \
    python-py-cpuinfo \
    python-pywlroots \
    qtile \
    rofi-calc \
    shellcheck \
    sway \
    swayidle \
    swaylock \
    ttf-anonymous-pro \
    ttf-font-awesome \
    ttf-nerd-fonts-symbols-mono \
    waybar \
    wl-clipboard \
    wofi \
    xautolock \


  # apps
  sudo pacman -Sy --needed \
    alacritty \
    atom \
    bc \
    emacs \
    exa \
    feh \
    ffmpeg \
    gparted \
    gimp \
    grim \
    jq \
    kitty \
    libvirt \
    mplayer \
    mpv \
    neofetch \
    nitrogen \
    qemu-arch-extra \
    ranger \
    screen \
    scrot \
    slurp \
    unzip \
    usbutils \
    vim \
    virt-manager \
    yad \
    youtube-dl \
    zip \

  # utils
  sudo pacman -Sy --needed \
    imagemagick \
    iw \
    lshw \
    nfs-utils \
    nmap \
    pacman-contrib \
    pulseaudio \
    python-beautifulsoup4 \
    system-config-printer \
    wget \

  # docker
  sudo pacman -Sy --needed \
    docker \

  if [ "$PRODUCT" == "MacBookPro5,5" ]
  then
    # lts kernel - useful to have on MacBookPro for failsafe
    sudo pacman -Sy --needed \
      linux-lts \
      linux-lts-headers \
      broadcom-wl-dkms
  fi

}

# -----------------------------------------------------------------------------
install_dwm()
{
  # download packages from https://gitlab.com/dwt1/
  # apply my patches to dwm and dwmblocks
  # make each and install
  echo "Installing DWM"; sleep 2

  pushd ~/clones || exit

  git clone http://gitlab.com/dwt1/dmenu-distrotube.git dmenu
  git clone http://gitlab.com/dwt1/dwmblocks-distrotube.git dwmblocks
  git clone http://gitlab.com/dwt1/dwm-distrotube.git dwm
  git clone http://gitlab.com/dwt1/st-distrotube.git st

  popd || exit
  cp dwm.patches/dwm.c.patch ~/clones/dwm/
  cp dwm.patches/Makefile.patch ~/clones/dwm/
  cp dwm.patches/blocks.def.h.patch ~/clones/dwmblocks/

  # dwm
  cd ~/clones/dwm || exit
  git checkout 12251a2
  patch < dwm.c.patch
  patch < Makefile.patch
  make
  sudo make install

  # dwmblocks
  cd ~/clones/dwmblocks || exit
  git checkout 92b2234
  patch < blocks.def.h.patch
  make
  sudo make install

  # dmenu
  cd ~/clones/dmenu || exit
  git checkout 75dfa57
  make
  sudo make install

  # st - terminal
  cd ~/clones/st || exit
  git checkout fee8c95
  make
  sudo make install

}


# -----------------------------------------------------------------------------
# install custom scripts/binaries
install_scripts()
{
  # install speedtest
  curl -sSL https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py  > /usr/local/bin/speedtest
  chmod +x /usr/local/bin/speedtest

  #local scripts=( have light )

  #for script in "${scripts[@]}"; do
  #        curl -sSL "https://misc.j3ss.co/binaries/$script" > "/usr/local/bin/${script}"
  #        chmod +x "/usr/local/bin/${script}"
  #done
}

# -----------------------------------------------------------------------------
install_something()
{
  echo "Install Some Stuff"
  echo "${INST_OPTS}"
  ${INST_OPTS}
}

# -----------------------------------------------------------------------------
install_everything()
{
  echo "Installing Everything"; sleep 2
  return

  # initial setup
  pacman_settings
  install_scripts

  # PACMAN
  install_pacman_packages

  # AUR
  install_yay_from_git
  install_aur_packages

  install_dwm
}

# -----------------------------------------------------------------------------
usage()
{
  echo "Usage:  install.sh"
  echo "    -h                  this help"
  echo "    -i <single option>  comma separated list of options to install"
  echo "    -a                  install all options, e.g. for a clean machine"
  echo
  echo "options available are"
  echo "  make_user_admin"
  echo "  pacman_settings"
  echo "  install_scripts"
  echo "  install_pacman_packages"
  echo "  install_yay_from_git"
  echo "  install_aur_packages"
  echo "  install_dwm"
  echo
}

# -----------------------------------------------------------------------------

[ $# -eq 0 ] && usage
while getopts "hi:a" o
do
  case "${o}" in
    'h' ) usage
          exit 0
          ;;
    'i' ) INST_OPTS=${OPTARG}
          install_something
          ;;
    'a' ) install_everything
          ;;
    *) usage
       ;;
  esac
done
shift $((OPTIND-1))

