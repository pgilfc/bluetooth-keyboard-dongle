#!/usr/bin/env bash

cp scripts/rc.local /etc/rc.local

chmod 755 /etc/rc.local

cp scripts/main.conf /etc/bluetooth/main.conf

echo "options btusb enable_autosuspend=n" > /etc/modprobe.d/btusb_disable_autosuspend.conf