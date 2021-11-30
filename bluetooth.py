import subprocess

class bluetoothctl:

    def power_bluetooth(self):
        subprocess.run("bluetoothctl power on", shell=True)

    def scan_start(self):
        return subprocess.Popen(["bluetoothctl", "scan", "on"])

    def scan_stop(self, process):
        process.terminate()

    def in_devices(self, mac_address):
        return mac_address in subprocess.run("bluetoothctl devices", shell=True, capture_output=True, text=True).stdout

    def in_paired_devices(self, mac_address):
        return mac_address in subprocess.run("bluetoothctl paired-devices", shell=True, capture_output=True, text=True).stdout

    def pair(self, mac_address):
        subprocess.run(["bluetoothctl", "pair", mac_address])
    
    def trust(self, mac_address):
        subprocess.run(["bluetoothctl", "trust", mac_address])

    def is_connected(self, mac_address):
        return "Connected: yes" in subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True).stdout
    
    def connect(self, mac_address):
        subprocess.run(["bluetoothctl", "connect", mac_address])
