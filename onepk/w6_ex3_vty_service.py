#! /usr/bin/env python

from pprint import pprint
from onepk_helper import NetworkDevice
from onep.vty import VtyService

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

    for dev in (pynet_rtr1, pynet_rtr2):

        rtr_obj = NetworkDevice(**dev)
        session_handle = rtr_obj.establish_session()

        vty_service = VtyService(rtr_obj.net_element)
        vty_service.open()

        CMD = "show version"
        cli = vty_service.write(CMD)

        print "\n\n"
        print rtr_obj.net_element.properties.sys_name
        print cli
 
        rtr_obj.disconnect()

if __name__ == '__main__':

    main()
