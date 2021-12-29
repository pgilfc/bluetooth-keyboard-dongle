
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

def start_stream(event):
    blocker = subprocess.Popen(["./input-event-blocker.out", event])
    stream = subprocess.Popen("exec cat {} > {}".format(HIDRAW, HIDG), shell=True)
    return blocker, stream

def stop_stream(blocker, stream):
    blocker.terminate()
    stream.terminate()

def read_config(filename):
    # import device mac address 
    datafile = open(filename, "r")
    config = datafile.read().strip(" ").strip("\n")
    datafile.close()
    return config

if __name__ == '__main__':

    #bypass "/sys/kernel/config/usb_gadget/mykeyboard" validation faster
    first_time_running = True

    # Kill possible blockers in the event of an app crash
    subprocess.run(["killall", "./input-event-blocker.out"])

    # import device mac address 
    address = read_config("MACADDRESS")

    # import stop_message
    stop_message = read_config("STOP_MESSAGE")
    len_stop_message = len(stop_message)

    # build input event blocker
    subprocess.run("gcc -o input-event-blocker.out input-event-blocker/input-event-blocker.c", shell=True)

    blu = bluetoothctl(address)

    while True:

        # power bluetooth
        blu.power_bluetooth()

        # check if connected with device
        while not blu.is_connected():
            sleep(2)

        # get input event
        event = get_input_event(address)
        if event == "":
            continue

        # init hid gadget
        if first_time_running and not os.path.exists("/sys/kernel/config/usb_gadget/mykeyboard"):
            subprocess.run(["modprobe", "libcomposite"])
            subprocess.run(["bash", "scripts/keyboard_config.sh", event])
            first_time_running = False

        while os.path.exists("/dev/input/{}".format(event)) and os.path.exists(HIDRAW):
            with open(HIDRAW, 'rb') as f:
                print("Starting stream")
                buf = b''
                blocker, stream = start_stream(event)
                stream_it = True
                while True:
                    try:
                        buf = buf + f.read(1)
                        while len(bintohex(buf)) > len_stop_message:
                            buf = buf[1:]
                        if bintohex(buf) == stop_message:
                            if stream_it:
                                stop_stream(blocker, stream)
                            else:
                                blocker, stream = start_stream(event)
                            stream_it = not stream_it
                            print("Streaming: ", stream_it)
                    except:
                        print("Something went wrong...")
                        break
                stop_stream(blocker, stream)
                print("Ending stream")
