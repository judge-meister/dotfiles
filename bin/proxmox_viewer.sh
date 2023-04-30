#!/bin/bash

#
# SETTINGS
#
# Fill the following section with your prefered settings.
# Leaving the password field empty is much more secure. It will be prompted on the command line.
# Alternatively create a Proxmox user with limited privileges like shown in this template.
#

NODE="192.168.0.30"
NODENAME="proxmox"
VMID="102"
PROXY=""
USERNAME="vdiuser@pve"
PASSWORD="wrac3eus"
VMSUPPLIED=0

if [ $# -gt 0 ]
then
  VMID="$1"
  VMSUPPLIED=1
fi

#
# INITIALIZATION
#

if ! type "jq" > /dev/null; then
    echo 'Command line tool "jq" is needed. Please install.'
fi

if [ -z "$PASSWORD" ]; then
    read -s -p "Password: " PASSWORD
    echo
fi

if [ -z "$USERNAME" ]; then
    USERNAME=root@pam
fi

if [ -z "$PROXY" ]; then
    PROXY=$NODE
fi

#
# AUTHENTICATION PROCESS
#

RESPONSE=$(curl -f -s -S -k -d "username=$USERNAME&password=$PASSWORD"  "https://$PROXY:8006/api2/json/access/ticket")

if [ $? -ne 0 ]; then
    echo "ERROR: Authentication failed"
    exit 1
fi

TICKET=$(echo $RESPONSE | jq -r '.data.ticket')
CSRF=$(echo $RESPONSE | jq -r '.data.CSRFPreventionToken')

if [ -z "$TICKET" ] || [ -z "$CSRF" ]; then
    echo "ERROR: Could not process Authentication Ticket"
    exit 1
fi

#
# GET LIST OF VMS IF NO PARAM SUPPLIED
#

if [ $VMSUPPLIED == 0 ]
then
  RESPONSE=$(curl -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/json/nodes/$NODENAME/qemu")

  VMIDS=($(echo $RESPONSE | jq -r '.data[].vmid'))
  NAMES=($(echo $RESPONSE | jq -r '.data[].name'))

  #echo ${VMIDS[@]}
  #echo ${NAMES[@]}

  CHOICES=""
  for vm in $( seq 1 ${#VMIDS[@]} )
  do
    CHOICES=$CHOICES" FALSE ${VMIDS[$((vm-1))]} \"${NAMES[$((vm-1))]}\""
  done
  vm_id=""
   
  vm_id=$(zenity --list --title "Choose a VM" --text "Choose a VM to view" --radiolist --column="" --column "VMID" --column "Name" $CHOICES)

  echo "[$vm_id]"
  if [ "$vm_id" != "" ]
  then
    VMID=$vm_id
  else
    exit
  fi
fi

echo $VMID

#
# GET VM STATUS
#

RESPONSE=$(curl -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/json/nodes/$NODENAME/qemu/$VMID/status/current")


STATUS=$(echo $RESPONSE | jq -r '.data.qmpstatus')

if [ $STATUS = "stopped" ]; then
    echo "ERROR: VM not running. Trying to start"
    RESPONSE=$(curl -d "" -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/json/nodes/$NODENAME/qemu/$VMID/status/start")

    echo "Waiting 10 seconds before trying Spice connection ..."
    sleep 10
fi

#
# GET SPICE CONFIGURATION
#

RESPONSE=$(curl -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/json/nodes/$NODENAME/qemu/$VMID/spiceproxy" -d "proxy=$PROXY")

if [ $? -ne 0 ]; then
    echo "ERROR: Maybe Proxmox-API changed?"
    exit 1
fi

#
# PARSING JSON RESPONSE
#

ATTENTION=$(echo $RESPONSE | jq -r '.data."secure-attention"')
DELETE=$(echo $RESPONSE | jq -r '.data."delete-this-file"')
PROXY=$(echo $RESPONSE | jq -r '.data.proxy')
TYPE=$(echo $RESPONSE | jq -r '.data.type')
CA=$(echo $RESPONSE | jq -r '.data.ca')
FULLSCREEN=$(echo $RESPONSE | jq -r '.data."toggle-fullscreen"')
TITLE=$(echo $RESPONSE | jq -r '.data.title')
HOST=$(echo $RESPONSE | jq -r '.data.host')
PASSWORD=$(echo $RESPONSE | jq -r '.data.password')
SUBJECT=$(echo $RESPONSE | jq -r '.data."host-subject"')
CURSOR=$(echo $RESPONSE | jq -r '.data."release-cursor"')
PORT=$(echo $RESPONSE | jq -r '.data."tls-port"')

#
# GENERATING REMOTE-VIEWER CONNECTION FILE
#

TMP=$(mktemp)

echo "[virt-viewer]" > $TMP
echo "secure-attention=${ATTENTION}" >> $TMP
echo "delete-this-file=${DELETE}" >> $TMP
echo "proxy=${PROXY}" >> $TMP
echo "type=${TYPE}" >> $TMP
echo "ca=${CA}" >> $TMP
echo "toggle-fullscreen=${FULLSCREEN}" >> $TMP
echo "title=${TITLE}" >> $TMP
echo "host=${HOST}" >> $TMP
echo "password=${PASSWORD}" >> $TMP
echo "host-subject=${SUBJECT}" >> $TMP
echo "release-cursor=${CURSOR}" >> $TMP
echo "tls-port=${PORT}" >> $TMP

#
# STARTING REMOTE-VIEWER
#

remote-viewer $TMP > ~/.tmp/remote_viewer.$$.log 2>&1 &

