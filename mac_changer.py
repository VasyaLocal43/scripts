import argparse
import subprocess
import sys

def change_mac(interface, new_mac):
    try:
        print(f"-> Shutting down {interface}")
        subprocess.check_call(f"sudo ifconfig {interface} down", shell=True)

        print(f"-> Changing MAC to {new_mac}")
        subprocess.check_call(f"sudo ifconfig {interface} hw ether {new_mac}", shell=True)

        print(f"-> Powering up {interface}")
        subprocess.check_call(f"sudo ifconfig {interface} up", shell=True)

        print("-> MAC address changed successfully")
        subprocess.call(f"sudo ifconfig {interface}", shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {e}")
        sys.exit(1)

# Set up argument parser
parser = argparse.ArgumentParser(description="Change the MAC address of a specified network interface.")
parser.add_argument("-i", "--interface", dest='interface', help="Interface to change MAC address", required=True)
parser.add_argument("-m", "--mac", dest='new_mac', help="New MAC address", required=True)
options = parser.parse_args()

# Validate input
interface = options.interface
new_mac = options.new_mac

if not interface or not new_mac:
    print("Error: Both interface and new MAC address must be provided.")
    sys.exit(1)

# Change the MAC address
change_mac(interface, new_mac)