import argparse
import subprocess
import shlex

# Create argument parser
parser = argparse.ArgumentParser(description="Search vulnerabilities web")
parser.add_argument("-ip", "--ip", dest='ip', default="127.0.0.1", help="IP or web address", required=True)
parser.add_argument("-protocol", "--protocol", dest='protocol', choices=["http", "https"], help="Protocol (http or https)", required=True)
parser.add_argument("-p", "--port", dest='port', default="-", help="Port", required=True)
options = parser.parse_args()

ip = options.ip
port = options.port
protocol = options.protocol

# Safe execution of commands with subprocess.run()
nmap_command = f"sudo nmap {ip} -p{port} -sV -sC --script=firewall-bypass,http-favicon,http-passwd,http-dombased-xss,http-auth,http-sql-injection,http-enum,exploit,vuln,http-fileupload-exploiter"
whatweb_command = f"whatweb -a 4 {protocol}://{ip}"
nikto_command = f"nikto -h {ip} -p {port}"


try:
    print("-> Running nmap scan...")
    with open(f"nmap_{ip}_{port}.txt", "w") as nmap_output:
        subprocess.run(shlex.split(nmap_command), stdout=nmap_output, check=True)
    print("[+] Nmap completed scanning")

    print("-> Running nikto scan...")
    with open(f"nikto_{ip}_{port}.txt", "w") as nikto_output:
        subprocess.run(shlex.split(nikto_command), stdout=nikto_output, check=True)
    print("[+] nikto completed scanning")

    print("-> Running whatweb scan...")
    with open(f"whatweb_{ip}_{port}.txt", "w") as whatweb_output:
        subprocess.run(shlex.split(whatweb_command), stdout=whatweb_output, check=True)
    print("[+] whatweb completed scanning")

except subprocess.CalledProcessError as e:
    print(f"An error occurred while running a command: {e}")
except FileNotFoundError as e:
    print(f"Command not found: {e}")

