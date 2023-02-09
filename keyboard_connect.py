
from bluetooth import bluetoothctl
from time import sleep
import os
import re
import subprocess

def is_connected(scan: str):
    return f"{address} Connected: yes" in scanv

def is_searching(scan: str):
    return f"{address} RSSI: " in scanv

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

        # this is for when the OS doesn't handle the connection
        while not blu.is_connected():
            scan_process = blu.scan_start()
            blu.connect()
            sleep(2) # to let the OS handle the connection
            scanv = blu.scan_stop(scan_process)
            print(scanv)
            sleep(1)
            # connection flicker (on and off instantly) or device is in search mode (and the connect above isnt working)
            if (is_connected(scanv) and not blu.is_connected()) or is_searching(scanv):
                print("connection has problems")
                # remove to enable connect_first_time again
                # WARNING: this could enable man in the middle (or other types of) attacks
                #blu.remove()
                #break

        # hold while connected
        print("connected")
        while blu.is_connected():
            sleep(1)
        print("disconnected")
