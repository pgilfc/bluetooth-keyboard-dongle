
from bluetooth import bluetoothctl
from time import sleep
import os
import re
import subprocess

blu = bluetoothctl()

# import device mac address 
datafile = open("MACADDRESS", "r")
address = datafile.read().strip(" ").strip("\n")
datafile.close()

# power bluetooth
blu.power_bluetooth()

# pair with device
if not blu.in_devices(address): # not paired
    scan_process = blu.scan_start() # start scan
    while not blu.in_paired_devices(address):
        blu.pair(address)
    blu.trust(address)
    blu.scan_stop(scan_process) # stop scan

# check if connected with device
while not blu.is_connected(address):
    blu.connect(address)
    sleep(2)

# check what device is the keyboard
path = '/sys/class/input'
regx = re.compile(r'^input[0-9]*$')
devices = list(filter(regx.search, os.listdir(path)))
regevent = re.compile(r'^event[0-9]*$')
event = ""
for dev in devices:
    dev_path = path+"/"+dev
    mac_file = dev_path+"/uniq"
    if os.path.isfile(mac_file):
        dbuff = open(mac_file, "r")
        dev_mac_addr = dbuff.read().strip(" ").strip("\n")
        dbuff.close()
        if dev_mac_addr == address.lower():
            events = list(filter(regevent.search, os.listdir(dev_path)))
            if len(events) > 0:
                event = events[0]
                break


# point device to usb output
if event != "":
    subprocess.run("cat /dev/input/"+event+" >> /dev/hidg0", shell=True)