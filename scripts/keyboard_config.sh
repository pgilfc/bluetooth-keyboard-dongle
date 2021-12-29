#!/bin/bash

# with help from https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition
# and https://github.com/torvalds/linux/blob/master/Documentation/usb/gadget_configfs.rst
# and http://eleccelerator.com/usbdescreqparser/
# and https://www.usb.org/hid

mkdir /sys/kernel/config/usb_gadget/mykeyboard
cd /sys/kernel/config/usb_gadget/mykeyboard

echo 0x0100 > bcdDevice # Version 1.0.0
echo 0x0200 > bcdUSB # USB 2.0
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceProtocol
echo 0x00 > bDeviceSubClass
echo 0x16 > bMaxPacketSize0
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x1d6b > idVendor # Linux Foundation

mkdir strings/0x409
echo "My manufacturer" > strings/0x409/manufacturer
echo "My virtual keyboard" > strings/0x409/product
echo "0123456789" > strings/0x409/serialnumber

mkdir functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 16 > functions/hid.usb0/report_length
echo 0 > functions/hid.usb0/subclass
# cp /sys/class/input/$1/device/device/report_descriptor functions/hid.usb0/report_desc
# this ^ didnt work for my usecase (keychron k2).
# it would work just fine in linux, however, in windows it would throw errors
# what i ended up doing was edit the report descriptor as to leave only the absolute necessary REPORT IDs (in this case 1 and 8)
# helpful commands:
# - xxd -i /sys/class/input/$1/device/device/report_descriptor (translate report descriptor to hex)
# - evtest (monitor keypresses)
# - cmp compare binary files
# if you need to use this, either replace the next line with the former line and test it
# or take some time to learn about HID descriptors and adapt it to your needs
cp /bluetooth-keyboard-auto-loader/scripts/report_desc functions/hid.usb0/report_desc

mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo 0x80 > configs/c.1/bmAttributes
echo 200 > configs/c.1/MaxPower # 200 mA
echo "Example configuration" > configs/c.1/strings/0x409/configuration

# Link HID function to configuration
ln -s functions/hid.usb0 configs/c.1

# Enable gadget
ls /sys/class/udc > UDC