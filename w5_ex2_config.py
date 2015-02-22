#!/usr/bin/env python

'''
v1.2

Using Arista's eapilib, create a script that allows you to add a VLAN (both the VLAN ID and the VLAN name).  Your script should first check that the VLAN ID is available and only add the VLAN if it doesn't already exist.  Use VLAN IDs between 100 and 999.  You should be able to call the script from the command line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably want to use Python's argparse to accomplish the argument processing.

'''

from pprint import pprint
import eapilib
import jsonrpclib
import argparse

eapi_params = dict ( 
    hostname='50.242.94.227', 
    port=8443, 
    username='eapi', 
    password='ZZteslaX'
    )

eapi_conn = eapilib.create_connection(**eapi_params)

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

def vlan_name_check(vlan_output, vlan_id, vlan_name):
    '''
    Searching "show vlan" output to determine if the vlan is named correctly
    '''
    
    vlan_name_correct = False

    if vlan_output['vlans'][vlan_id]['name'] == vlan_name:
        vlan_name_correct = True
    return vlan_name_correct

def vlan_id_check(vlan_output, vlan_id):
    '''
    command "show vlan" returns a list with a single element.  That
    single element is a dictionary of key:value pairs (wich are nested dicts) 
    that is the desired vlan data.  With that dict, we will search to see if 
    the vlan number and vlan name exist
    '''

#    response = remote_connect.runCmds(1, ['show vlan'])[0]

    try:
        x = vlan_output['vlans'][vlan_id]
        vlan_exists = True
    except:
        vlan_exists = False
    return vlan_exists

def main():

    commands =[]

    vlan_output = eapi_conn.run_commands(['show vlan'])[0]
    # Argument parse function
    configlets, add_vlan, name_vlan, remove_vlan = arg_parse()

    # For each arg, create commands string
    if configlets:
        for item in configlets:
            commands.append(item)

    if add_vlan:
        vlan_exists = vlan_id_check(vlan_output, add_vlan)
        if not vlan_exists:
            commands.append('vlan ' + add_vlan)
            if name_vlan:
                commands.append('name ' + name_vlan)
    if remove_vlan:
        commands.append('no vlan ' + remove_vlan)

    # Apply configuration to device
    eapi_conn.config(commands)

if __name__ == '__main__':

    main()
