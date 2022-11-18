# Functions:

def interface(defRouter,e1,e2,description1,description2):
    IFconfig_commands = [
                        f"set interfaces ethernet {e2} address '{defRouter}/24'",
                        f"set interfaces ethernet {e1} description {description1}",
                        f"set interfaces ethernet {e2} description {description2}",
                        ]
    return IFconfig_commands

def dhcp(name,subnet,defRouter,domain,leaseTime,id,startRange,stopRange):

    DHCPconfig_commands = [ f"set service dhcp-server shared-network-name {name} subnet {subnet} default-router '{defRouter}'",
                        f"set service dhcp-server shared-network-name {name} subnet {subnet} domain-name '{domain}'",
                        f"set service dhcp-server shared-network-name {name} subnet {subnet} lease '{leaseTime}'",
                        f"set service dhcp-server shared-network-name {name} subnet {subnet} range {id} start {startRange}",
                        f"set service dhcp-server shared-network-name {name} subnet {subnet} range {id} stop '{stopRange}'",
                        ]
    return DHCPconfig_commands

def dns(dnsCache,defRouter,subnet):

    DNSconfig_commands = [f"set service dns forwarding cache-size '{dnsCache}'",
                        f"set service dns forwarding listen-address '{defRouter}'",
                        f"set service dns forwarding allow-from '{subnet}'",
                        ]
    return DNSconfig_commands

def nat(ruleNumber,e1,subnet):

    NATconfig_commands = [f"set nat source rule {ruleNumber} outbound-interface '{e1}'",
                        f"set nat source rule {ruleNumber} source address '{subnet}'",
                        f"set nat source rule {ruleNumber} translation address masquerade",
                        ]
    return NATconfig_commands
