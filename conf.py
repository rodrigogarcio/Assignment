import netmiko
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
import argparse
import os
import ref

# Parsing the Values:

parser = argparse.ArgumentParser(
    description="Provide the required arguments",
    prefix_chars="-"
)

parser.add_argument(
    '-t',
    type=str,
    nargs='+',
    required=True,
    help="Device Type name"
)

parser.add_argument(
    '-ip',
    type=str,
    nargs='+',
    required=True,
    help="Device IP Address"
)

parser.add_argument(
    '-u',
    type=str,
    nargs='+',
    required=True,
    help="Device Username"
)

parser.add_argument(
    '-p',
    type=str,
    nargs='+',
    required=True,
    help="Device Password"
)

parser.add_argument(
    '-port',
    type=int,
    nargs='+',
    required=True,
    help="Device Port Number"
)

args = vars(parser.parse_args())

deviceType = args['t'].pop(0)
ipaddr = args['ip'].pop(0)
usrname = args['u'].pop(0)
passwd = args['p'].pop(0)
port = args['port'].pop(0)

# VyOS Router Initial Config:

vyosRouter = {
  "device_type": deviceType,
  "host": ipaddr,
  "username": usrname,
  "password": passwd,
  "port": port
  }

vyos_connection = ConnectHandler(**vyosRouter)

# Choose what to configure:

print("""
----------------------------------
Configuring the Services you want:
----------------------------------
""")

## Mandatory Configuration:

print("""

            Step 1
------------------------------------
Configuring the Ethernet Interfaces
------------------------------------
""")

st_eth = input("Select the name of the first ethernet adapter: ")
nd_eth = input("Select the name of the second ethernet adapter: ")
desc1 = input("Description for the first ethernet adaptor: ")
desc2 = input("Description for the second ethernet adaptor: ")
subnet_addr = input("Please provide the subnet address space (CIDR included): ")
def_route = input("Specify the gateway IP Address for your subnet: ")

ifconfig = ref.interface(def_route,st_eth,nd_eth,desc1,desc2)

## Optional Configuration:

print("""

            Step 2
------------------------------------
Configuring the DHCP
------------------------------------
""")

choice1 = input("Do you want to configure the DHCP service? [yes or no]  ")

if choice1 == 'yes' or choice1 == 'y':
    sh_name = input("Specify the name of the shared network: ")
    dm = input("Provide a domain name: [example.com]  ")
    lease = input("Provide the lease time, in seconds, for IP Assignment: [default:86400]  ")
    range_id = input("Provide the ID range number: ")
    start = input("Specify the first available address of the DHCP pool: ")
    stop = input("Specify the last available address of the DHCP pool: ")

    dhcpconfig = ref.dhcp(sh_name,subnet_addr,def_route,dm,lease,range_id,start,stop)
else:
    print("Moving to the next Step")

print("""

            Step 3
------------------------------------
Configuring the DNS
------------------------------------
""")

choice2 = input ("Do you want to configure the DNS service? [yes or no]  ")

if choice2 == 'yes' or choice2 == 'y':
    cache = input("Specify the number of cache entries: [0-2147483647]  ")

    dnsconfig = ref.dns(cache,def_route,subnet_addr)
else:
    print("Moving to the next Step")

print("""

            Step 4
------------------------------------
Configuring the NAT
------------------------------------
""")

choice3 = input ("Do you want to configure the NAT service? [yes or no]  ")

if choice3 == 'yes' or choice3 == 'y':
    rule = input("Specify the rule number for network address translation: ")

    natconfig = ref.nat(rule,st_eth,subnet_addr)
else:
    print("End of initial configuration")

print("""

            Step 5
------------------------------------
Commiting the Previous Configuration
------------------------------------
""")

# Testing all the Variables:

if_out = vyos_connection.send_config_set(ifconfig,exit_config_mode=False) # Variable will always be created

try:
    dhcp_out = vyos_connection.send_config_set(dhcpconfig,exit_config_mode=False)
    dns_out = vyos_connection.send_config_set(dnsconfig,exit_config_mode=False)
    nat_out = vyos_connection.send_config_set(natconfig,exit_config_mode=False)
except (NameError,ValueError):
    print("\nSome Variables were not Created\n")

# Display the Variables:

try:
    print(ifconfig)
    print(dhcpconfig)
    print(dnsconfig)
    print(natconfig)
except (NameError,ValueError):
    print("\nSome Variables were not Created\n")

# Commit Configuration:

commit_out = vyos_connection.commit()

# Displaying information about the configuration:

show_if = vyos_connection.send_command("run show interfaces ethernet")
show_config = vyos_connection.send_command("run show config")

# Saving the output information in a .txt file: 

myPath = os.getcwd()

out_file = open(myPath+'\\output.txt', 'a')

out_list = []

if choice1 == 'yes' and choice2 == 'yes' and choice3 == 'yes' or choice1 == 'y' and choice2 == 'y' and choice3 == 'y':
    out_list = [if_out]
    out_list.extend([dhcp_out,dns_out,nat_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice1 == 'yes' and choice2 == 'yes' or choice1 == 'y' and choice2 == 'y':
    out_list = [if_out]
    out_list.extend([dhcp_out,dns_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice1 == 'yes' and choice3 == 'yes' or choice1 == 'y' and choice3 == 'y':
    out_list = [if_out]
    out_list.extend([dhcp_out,nat_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice2 == 'yes' and choice3 == 'yes' or choice2 == 'y' and choice3 == 'y':
    out_list = [if_out]
    out_list.extend([dns_out,nat_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice1 == 'yes' or choice1 == 'y':
    out_list = [if_out]
    out_list.extend([dhcp_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice2 == 'yes' or choice2 == 'y':
    out_list = [if_out]
    out_list.extend([dns_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
elif choice3 == 'yes' or choice3 == 'y':
    out_list = [if_out]
    out_list.extend([nat_out,commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)
else:
    out_list = [if_out]
    out_list.extend([commit_out,show_if,show_config])

    for o in out_list:
        out_file.write("\n"+o)

out_file.close()