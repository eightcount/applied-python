#! /usr/bin/env python

'''
Using the onepk_helper library establish a onePK connection to one
 of the two lab routers.  From this lab router obtain the product_id
 and SerialNo:
'''

from onepk_helper import NetworkDevice

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
        # call to NetworkDevice class
        rtr_obj = NetworkDevice(**dev)

        # creates connection to router
        session_handle = rtr_obj.establish_session()

        # stuff we want to know
        model = rtr_obj.net_element.properties.product_id
        serial_no = rtr_obj.net_element.properties.SerialNo

        print "\n\n"
        print rtr_obj.net_element.properties.sys_name
        print "Model: {}".format(model)
        print "Serial Number: {}".format(serial_no)
        print "\n"

        # disconnect connection
        rtr_obj.disconnect()

if __name__ == '__main__':

    main()
