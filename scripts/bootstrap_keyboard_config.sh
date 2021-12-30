#!/usr/bin/env bash

# $1 is suposed to be the root filesystem
# $2 is suposed to be the /boot filesystem

echo "dtoverlay=dwc2" >> $2/config.txt

mkdir $1/bluetooth-keyboard-dongle

cp -R . $1/bluetooth-keyboard-dongle

cp scripts/main.conf $1/etc/bluetooth/main.conf

echo "options btusb enable_autosuspend=n" > $1/etc/modprobe.d/btusb_disable_autosuspend.conf

cp systemd/bluetooth-keyboard-bypass.service $1/etc/systemd/system/bluetooth-keyboard-bypass.service

cp systemd/bluetooth-keyboard-connect.service $1/etc/systemd/system/bluetooth-keyboard-connect.service

cd $1/etc/systemd/system/multi-user.target.wants/

ln -s ../bluetooth-keyboard-bypass.service bluetooth-keyboard-bypass.service

ln -s ../bluetooth-keyboard-connect.service bluetooth-keyboard-connect.service