
from bluetooth import bluetoothctl
from time import sleep
import os
import re
import subprocess

if __name__ == '__main__':
    # import device mac address 
    datafile = open("MACADDRESS", "r")
    address = datafile.read().strip(" ").strip("\n")
    datafile.close()
    while True:
        blu = bluetoothctl()

        # power bluetooth
        blu.power_bluetooth()

        # pair with device
        while not blu.in_paired_devices(address): # not paired
            scan_process = blu.scan_start() # start scan
            sleep(2)
            blu.scan_stop(scan_process) # stop scan
            print(scan_process.stdout.read().decode('utf-8'))
            if blu.in_devices(address):
                blu.trust(address)
                blu.pair(address)
                blu.connect(address)

        # hold
        while blu.is_connected(address):
            sleep(5)