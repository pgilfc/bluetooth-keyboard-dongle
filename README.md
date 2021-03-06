# Bluetooth Keyboard Dongle

Scripts to auto pair a bluetooth keyboard to current device and hook it to the usb output on a pi zero.

Basically a usb dongle for a dongless usb keyboard.

This works on my Keychron k2 wireless keyboard.

For other keyboards you might need to change the report description (among other things) in the scripts/keyboard_config.sh file.

## Use Case
1. I have a KVM.
2. Bluetooth keyboard doesn't have an usb dongle.
3. Regular usb dongles don't work, because the connection is managed by the OS.
4. I don't want to keep pairing the keyboard to each computer everytime i switch the kvm.
5. This way I can use the KVM keyboard shortcuts.
6. Why the hell not.

## Requirements
* bluetoothctl
* gcc
* python3
* systemd
* GNU
* linux
* rbp zero w

## Getting started
* Flash a light distro into the sd card.
* Create a MACADDRESS file with your device's mac address
* Run `git submodule update --init --recursive`
* Run `bootstrap_keyboard_config.sh` to get micro sd ready to boot.
    * Ex.: `bash scripts/bootstrap_keyboard_config.sh /mnt/rootfs /mnt/boot`
## Report Descriptor
If you have a keychron k2, this should probably work as is.

Otherwise... well just read `scripts/keyboard_config.sh`...

`scripts/report_desc` is the report descriptor I am currently using.

The hex version of that same file is in scripts/report_desc_hex.

## Stop Message
The stop message is intended to stop the keyboard bypass and allow you to regain controll of the raspberry pi (only makes sense if NOT using the pi fully headless).

Stop message will depend on your keyboard's report description.

`STOP_MESSAGE` file might need to be adapted to use case.

Currently it's -> left shift, left ctrl, left special, left alt, right alt, right ctrl
