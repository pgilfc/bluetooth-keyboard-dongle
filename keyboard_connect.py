
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
    blu = bluetoothctl(address)
    while True:

        # power bluetooth
        blu.power_bluetooth()

        scan_process = blu.scan_start() # start scan
        # initial pair with device (or after it's "deleted")
        while not blu.is_trusted(): # should be trusted to be permanent
            if blu.in_devices(): # is in devices if it has been paired before or if it's in scaning mode
                blu.connect_first_time()
        print(blu.scan_stop(scan_process)) # stop scan
        #print(scan_process.stdout.read().decode('utf-8'))

        # hold while connected
        while blu.is_connected():
            sleep(6)
