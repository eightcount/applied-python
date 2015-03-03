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

    # call to NetworkDevice class
    rtr1_obj = NetworkDevice(**pynet_rtr1)

    # creates connection to router
    session_handle1 = rtr1_obj.establish_session()

    # stuff we want to know
    model = rtr1_obj.net_element.properties.product_id
    serial_no = rtr1_obj.net_element.properties.SerialNo

    # disconnect connection
    rtr1_obj.disconnect()

    print "\n\n"
    print "Model: {}".format(model)
    print "Serial Number: {}".format(serial_no)
    print "\n"


if __name__ == '__main__':

    main()
