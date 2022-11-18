# Introduction
Create a command line interface where you can enter values to configure selected services and properties for a vyos device.
The script should be able to connect to the vyos device at a user specified IPv4 address.
The script should be able to configure interface descriptions, enable NAT, configure DHCP services with user-specified scope addresses, and/or enable DNS resolution. 
The user should be able to choose any of these configuration options through some method of user input, such as parameters.

# How to use the program

- Usage: conf.py [-h] -t [DeviceType] -ip [IPAddress] -u [Username] -p [Password] -port [PORT]
    
    Provide the required arguments

    options:
    -h, --help              show this help message and exit
    -t                      Device Type name
    -ip                     Device IP Address
    -u                      Device Username
    -p                      Device Password
    -port                   Device Port Number

    * REQUIRED: All the following arguments are required: -t, -ip, -u, -p, -port

# Description
The VyOS device should have at least one IP Address configured and port 22 (SSH) enabled in order for this code to run properly.

# Features
To initiate the connection with the VyOS device, the user will pass the initial values through the CLI, assuming that it already knows the IP Address of the machine.

Once the connection has been stablished, the user will be prompted with some question that will be applied to the network device.

At the end of the process, a .txt file will be created and it will contain the outputs and configuration files that were successfully deployed.

# Complete Configuration Example:    
    
    python conf.py -t vyos -ip 10.0.0.6 -u vyos -p vyos -port 22


    ----------------------------------
    Configuring the Services you want:
    ----------------------------------



                Step 1
    ------------------------------------
    Configuring the Ethernet Interfaces
    ------------------------------------

    Select the name of the first ethernet adapter: eth0
    Select the name of the second ethernet adapter: eth1
    Description for the first ethernet adaptor: WAN
    Description for the second ethernet adaptor: LAN
    Please provide the subnet address space (CIDR included): 10.200.6.0/24
    Specify the gateway IP Address for your subnet: 10.200.6.1


                Step 2
    ------------------------------------
    Configuring the DHCP
    ------------------------------------

    Do you want to configure the DHCP service? [yes or no]  y
    Specify the name of the shared network: LAN
    Provide a domain name: [example.com]  vyos.net
    Provide the lease time, in seconds, for IP Assignment: [default:86400]  86400
    Provide the ID range number: 0
    Specify the first available address of the DHCP pool: 10.200.6.10
    Specify the last available address of the DHCP pool: 10.200.6.100


                Step 3
    ------------------------------------
    Configuring the DNS
    ------------------------------------

    Do you want to configure the DNS service? [yes or no]  y
    Specify the number of cache entries: [0-2147483647]  0


                Step 4
    ------------------------------------
    Configuring the NAT
    ------------------------------------

    Do you want to configure the NAT service? [yes or no]  y
    Specify the rule number for network address translation: 150


                Step 5
    ------------------------------------
    Commiting the Previous Configuration
    ------------------------------------

    ["set interfaces ethernet eth1 address '10.200.6.1/24'", 'set interfaces ethernet eth0 description WAN', 'set interfaces ethernet eth1 description LAN']
    ["set service dhcp-server shared-network-name LAN subnet 10.200.6.0/24 default-router '10.200.6.1'", "set service dhcp-server shared-network-name LAN subnet 10.200.6.0/24 domain-name 'vyos.net'", "set service 
    dhcp-server shared-network-name LAN subnet 10.200.6.0/24 lease '86400'", 'set service dhcp-server shared-network-name LAN subnet 10.200.6.0/24 range 0 start 10.200.6.10', "set service dhcp-server shared-network-name LAN subnet 10.200.6.0/24 range 0 stop '10.200.6.100'"]
    ["set service dns forwarding cache-size '0'", "set service dns forwarding listen-address '10.200.6.1'", "set service dns forwarding allow-from '10.200.6.0/24'"]
    ["set nat source rule 150 outbound-interface 'eth0'", "set nat source rule 150 source address '10.200.6.0/24'", 'set nat source rule 150 translation address masquerade']