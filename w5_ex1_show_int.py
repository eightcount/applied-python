'''
Use Arista's eAPI to obtain 'show interfaces' from the switch.  Parse the 'show interfaces' output to obtain the 'inOctets' and 'outOctets' fields for each of the interfaces on the switch.  Accomplish this directly using jsonrpclib.
'''

import jsonrpclib

# Variables
ip = '50.242.94.227'
port = '8243'
username = 'eapi'
password = '99saturday'

# Syntax to send eapi commands
switch_url = 'https://{}:{}@{}:{}'.format(username, password, ip, port)
switch_url = switch_url + '/command-api'
remote_connect = jsonrpclib.Server(switch_url)
response = remote_connect.runCmds(1, ['show interfaces'])

def interface_counters(dict, interface, object):
# Retrieves values tied to desired counters
    value = dict[interface]['interfaceCounters'][object]
    return value    

def main():

    # Create dictionary with interface as key and statistics as value
    all_int_stats = response[0]['interfaces']

    # Iterate over key:value pairs
    for interface,int_stats in all_int_stats.items():

        # Iterate over interface attributes and their values
        for int_att,v in int_stats.items():

            # Identify interface counters and collect desired data
            if int_att == 'interfaceCounters':
                in_octets = interface_counters(all_int_stats, interface, 'inOctets')
                out_octets = interface_counters(all_int_stats, interface, 'outOctets')

                # Output
                print "{}: IN:{} OUT:{}".format(interface, in_octets, out_octets)            

main()    
