import subprocess

class bluetoothctl:

    def __init__(self, mac_address):
        self.mac_address = mac_address

    def power_bluetooth(self):
        subprocess.run(["bluetoothctl", "power", "on"])

    def scan_start(self) -> subprocess.Popen[bytes]:
        return subprocess.Popen(["bluetoothctl", "scan", "on"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    def scan_stop(self, process: subprocess.Popen[bytes]) -> str:
        process.terminate()
        return process.communicate()[0].decode('utf-8')

    def in_devices(self):
        return self.mac_address in subprocess.run("bluetoothctl devices", shell=True, capture_output=True, text=True).stdout

    def in_paired_devices(self):
        return self.mac_address in subprocess.run("bluetoothctl paired-devices", shell=True, capture_output=True, text=True).stdout

    def connect_first_time(self): # for connection to persist, all the commands needed to be run inside bluetoothctl
        subprocess.run(["bash", "./scripts/bluetooth_connect_first_time.sh", self.mac_address])

    def info(self):
        return subprocess.run(["bluetoothctl", "info", self.mac_address], capture_output=True, text=True).stdout

    def is_connected(self):
        return "Connected: yes" in self.info()

    def is_trusted(self):
        return "Trusted: yes" in self.info()

    def remove(self):
        subprocess.run(["bluetoothctl", "remove", self.mac_address])

    def connect(self):
        subprocess.run(["bluetoothctl", "connect", self.mac_address])
