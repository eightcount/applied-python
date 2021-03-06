#! /usr/bin/env python

from pprint import pprint
from onepk_helper import NetworkDevice
from onep.interfaces import NetworkInterface
from onep.interfaces import InterfaceFilter

def main():

    # define device properties
    pynet_rtr1 = dict(
        ip = '50.242.94.227',
        username = 'pyclass',
        password = '88newclass',
        pin_file = 'pynet-rtr1-pin.txt',
        port = 15002
    )

    pynet_rtr2 = dict(
        ip = '50.242.94.227',
        username = 'pyclass',
        password = '88newclass',
        pin_file = 'pynet-rtr2-pin.txt',
        port = 8002
    )

    InterfaceTypes = NetworkInterface.InterfaceTypes
    filter = InterfaceFilter(None,InterfaceTypes.ONEP_IF_TYPE_ETHERNET)

    for dev in (pynet_rtr1, pynet_rtr2):

        rtr_obj = NetworkDevice(**dev)
        session_handle = rtr_obj.establish_session()

        intf = rtr_obj.net_element.get_interface_list(filter)[0]
        int_stats = intf.get_statistics()

        print "\n\n"
        print rtr_obj.net_element.properties.sys_name
        print "\n"
        print int_stats
        rtr_obj.disconnect()

if __name__ == '__main__':

    main()
