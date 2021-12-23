
from bluetooth import bluetoothctl
from time import sleep
import subprocess
import os
import re

HIDRAW = "/dev/hidraw0"
HIDG = "/dev/hidg0"

def bintohex(data):
    return "\\"+"\\".join(list(("x" if "%x"%x !="0" else "") + "%x"% x for x in data))

def get_input_event(address):
    # returns device input event
    event = ""
    path = '/sys/class/input'
    regx = re.compile(r'^input[0-9]*$')
    devices = list(filter(regx.search, os.listdir(path)))
    regevent = re.compile(r'^event[0-9]*$')
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
    return event

if __name__ == '__main__':

    stream_it = True

    # import device mac address 
    datafile = open("MACADDRESS", "r")
    address = datafile.read().strip(" ").strip("\n")
    datafile.close()

    # build input event blocker
    subprocess.run("gcc -o input-event-blocker.out input-event-blocker/input-event-blocker.c", shell=True)

    blu = bluetoothctl(address)

    while True:

        # power bluetooth
        blu.power_bluetooth()

        # check if connected with device
        while not blu.is_connected():
            sleep(2)

        event = get_input_event(address)

        if event != "" and os.path.exists(HIDRAW):
            with open(HIDRAW, 'rb') as f, open(HIDG,"wb") as out:
                blocker = subprocess.Popen(["./input-event-blocker.out", event])
                while os.path.exists(HIDRAW):
                    buf = f.read(6)
                    if hex(buf[0]) == "0x1":
                        head = buf[1:]
                        buf = f.read(5)
                        message = bintohex(head + buf[:-2])
                        if message == "\\x5f\\0\\0\\0\\0\\0\\0\\0": # left shift, left ctrl, left special, left alt, right alt, right ctrl
                            if stream_it:
                                blocker.terminate()
                            else:
                                blocker = subprocess.Popen(["./input-event-blocker.out", event])
                            stream_it = not stream_it
                    elif hex(buf[0]) == "0x8":
                        message = "\\0\\0\\x" + "%x"%buf[1] + "\\0\\0\\0\\0\\0"
                    else:
                        message = "\\0\\0\\0\\0\\0\\0\\0\\0"
                    if stream_it:
                        subprocess.run(["echo", "-ne", message], stdout=out)
