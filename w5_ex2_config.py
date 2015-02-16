'''

Using Arista's eapilib, create a script that allows you to add a VLAN (both the VLAN ID and the VLAN name).  Your script should first check that the VLAN ID is available and only add the VLAN if it doesn't already exist.  Use VLAN IDs between 100 and 999.  You should be able to call the script from the command line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably want to use Python's argparse to accomplish the argument processing.

'''

from pprint import pprint
import jsonrpclib
import argparse

# Variables
ip = '50.242.94.227'
port = '8443'
username = 'eapi'
password = 'ZZteslaX'

# Syntax to send eapi commands
switch_url = 'https://{}:{}@{}:{}'.format(username, password, ip, port)
switch_url = switch_url + '/command-api'
remote_connect = jsonrpclib.Server(switch_url)

def arg_parse():
# CLI argument parse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs='+', 
                         help='Quoted commands')
    parser.add_argument('-v', '--vlan', help='VLAN #')
    parser.add_argument('-n', '--name', help='VLAN name')
    parser.add_argument('-r', '--remove', help='Delete vlan')

    # Variables for each arg
    configlets = parser.parse_args().config
    add_vlan = parser.parse_args().vlan
    name_vlan = parser.parse_args().name
    remove_vlan = parser.parse_args().remove

    return (configlets, add_vlan, name_vlan, remove_vlan) 

def check_conf(vlan):
    # Dict with vlan:attribute key:value pair
    response = remote_connect.runCmds(1, ['show vlan'])[0]
    # Check if vlan exists
    try:
        x = response['vlans'][vlan]
        vlan_exists = True
    except:
        vlan_exists = False
    return vlan_exists

def main():

    # Default commands to configure device
    commands = [{'input': '', 'cmd': 'enable'}, 'configure terminal']

    # Argument parse function
    configlets, add_vlan, name_vlan, remove_vlan = arg_parse()

    # For each arg, create commands string
    if configlets:
        for item in configlets:
            commands.append(item)

    if add_vlan:
        vlan_exists = check_conf(add_vlan)
        if not vlan_exists:
            commands.append('vlan ' + add_vlan)
            if name_vlan:
                commands.append('name ' + name_vlan)
    if remove_vlan:
        commands.append('no vlan ' + remove_vlan)

    # Apply configuration to device
    remote_connect.runCmds(1, commands)

if __name__ == '__main__':

    main()
