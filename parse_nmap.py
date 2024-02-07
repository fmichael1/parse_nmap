# hello
import subprocess
import re
import socket
import struct
import socket
import subprocess

def get_network_ssid():
    """ Get the SSID of the connected Wi-Fi network (macOS). """
    try:
        result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport", "-I"], text=True)
        for line in result.splitlines():
            if " SSID:" in line:
                return line.split(":")[1].strip()
    except subprocess.CalledProcessError:
        return "Unknown"

def get_subnet_mask(ip):
    """ A simple method to calculate the subnet mask for /24 networks. """
    return "255.255.255.0"  # Assuming /24 subnet mask

def get_network_gateway():
    """ Get the default gateway (network gateway). """
    try:
        result = subprocess.check_output(["netstat", "-nr"], text=True)
        lines = result.splitlines()
        for line in lines:
            if line.startswith('default') or 'default' in line:
                return line.split()[1]
    except subprocess.CalledProcessError:
        return "Unknown"

# Set a default timeout of 2 seconds for all socket operations
socket.setdefaulttimeout(2)

def get_local_ip():
    """ Get the local IP address of the computer running this script. """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def ip_to_network(ip):
    """ Convert an IP address to a network address with /24 subnet. """
    return ip[:ip.rfind('.')] + '.0/24'


import subprocess

def get_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror, socket.timeout):
        # Try mDNS lookup as a fallback (using dns-sd or avahi-browse)
        mdns_output = run_mdns_lookup(ip)
        hostname = parse_dns_sd_output(mdns_output)  # or parse_avahi_output(mdns_output) on Linux
        if hostname != "Unknown":
            return hostname

        # Try NetBIOS lookup as a second fallback
        netbios_output = run_netbios_lookup(ip)
        hostname = parse_nmblookup_output(netbios_output)
        return hostname

# Implement run_mdns_lookup and run_netbios_lookup to execute the respective commands
# and return their outputs. You will need to use subprocess.check_output similar to the 
# existing run_nmap function.


def mdns_lookup(ip):
    try:
        # Using dns-sd for mDNS lookup (common on macOS)
        # For Linux, you might use 'avahi-browse' instead
        result = subprocess.check_output(["dns-sd", "-G", "v4", ip], timeout=2, text=True)
        # Parse result to extract hostname
        # Add parsing logic based on the output format
        return "Extracted Hostname"  # Replace with actual extraction logic
    except Exception:
        return "Unknown"

def netbios_lookup(ip):
    try:
        result = subprocess.check_output(["nmblookup", "-A", ip], timeout=2, text=True)
        # Parse result to extract hostname
        # Add parsing logic based on the output format
        return "Extracted Hostname"  # Replace with actual extraction logic
    except Exception:
        return "Unknown"

def parse_dns_sd_output(output):
    for line in output.splitlines():
        if "can be reached at" in line:
            # Extract and return the hostname from the line
            hostname = line.split(' ')[0]
            return hostname
    return "Unknown"


def parse_nmblookup_output(output):
    for line in output.splitlines():
        if "<00>" in line:
            # Extract and return the NetBIOS name from the line
            parts = line.split(' ')
            hostname = parts[0]  # Assuming hostname is the first part
            return hostname
    return "Unknown"



def get_my_hostname():
    """ Get the hostname of the local machine. """
    return socket.gethostname()



def run_nmap(network):
    """ Run the nmap scan and return the output. """
    try:
        output = subprocess.check_output(['nmap', '-T4', '-F', network], text=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to run nmap: {e}")
        return ""

def parse_nmap_output(nmap_output):
    ip_regex = r"Nmap scan report for ([\d\.]+)"
    port_regex = r"(\d+/tcp)\s+\w+\s+(\w+)"  # Modified to capture port and service
    lines = nmap_output.strip().split("\n")
    hosts = []
    current_host = {}

    for line in lines:
        ip_match = re.search(ip_regex, line)
        if ip_match:
            if current_host:
                hosts.append(current_host)
            current_host = {"IP Address": ip_match.group(1), "Hostname": "Unknown", "Ports": []}
        port_match = re.search(port_regex, line)
        if port_match:
            port_info = f"{port_match.group(1)} ({port_match.group(2)})"  # Formatting as 'port (service)'
            current_host["Ports"].append(port_info)
    if current_host:
        hosts.append(current_host)
    return hosts


# Main execution
ssid = get_network_ssid()
local_ip = get_local_ip()
my_hostname = get_my_hostname()  # Get the hostname of your machine
subnet_mask = get_subnet_mask(local_ip)  # You already have local_ip from get_local_ip()
gateway = get_network_gateway()
network = ip_to_network(local_ip)

# Printing network details with tabs for alignment
print(f"Network SSID:\t\t{ssid}")
print(f"Subnet Mask:\t\t{subnet_mask}")
print(f"Network Gateway:\t{gateway}")
print(f"My IP:\t\t\t{local_ip} ({my_hostname})")
print()



# Continue with nmap scanning and parsing...
nmap_output = run_nmap(network)
hosts = parse_nmap_output(nmap_output)


print(f"{'Host':<5}{'IP Address':<16}{'Hostname':<20}{'Ports':<30}")
print("-" * 70)  # Prints a line for visual separation

for i, host in enumerate(hosts, 1):
    # Prepare the first line with host number, IP, and hostname
    first_line = f"{i:<5}{host['IP Address']:<16}{host['Hostname']:<20}"
    if host["Ports"]:
        # Add the first port to the first line
        first_line += f"{host['Ports'][0]:<30}"
        print(first_line)
        # Print remaining ports, if any, on new lines aligned with the ports column
        for port in host["Ports"][1:]:
            print(f"{'':<41}{port:<30}")
    else:
        # If there are no ports, just print the first line
        print(first_line)
    print("-" * 70) # Adds an extra newline for better separation between hosts


