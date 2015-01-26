'''
Using SNMPv3 create two SVG image files.  The first image file should graph input and output octets on interface FA4 on pynet-rtr1 every five minutes for an hour.  Use the pygal library to create the SVG graph file.  

The second SVG graph file should be the same as the first except graph unicast packets received and transmitted.

The relevant OIDs are as follows:

('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')

'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
import os.path
import pickle
import pygal

def graph_data(device_a, ifdescr):

  file_name = "/home/pperreault/classwork/files/" + device_a[0] + "_" + ifdescr + ".pkl"
  f = open(file_name, "rb")

  # Retrieve raw data from pickle file
  in_oct_raw = pickle.load(f)
  out_oct_raw = pickle.load(f)
  in_ucast_raw = pickle.load(f)
  out_ucast_raw = pickle.load(f)

  f.close()

  # Manage values to be graphed with two lists
  # counter_list holds the raw data
  counter_list = in_oct_raw, out_oct_raw, in_ucast_raw, out_ucast_raw

  # list for time period deltas
  graph_list = []

  for counter in counter_list:
    # Creating two temp lists to manage data
    # NOTE:Seems like redundant use of lists, would love to be more efficient
    tmp = counter
    tmp2 = []

    # Iterate over list of raw values
    for i in range(len(tmp)):
      # Skip the 0 place
      if i == 0:
        continue
      # Subtract N-1 from Nth value to get utilization
      delta = int(tmp[i]) - int(tmp[i-1])
      tmp2.append(delta)
    graph_list.append(tmp2)

  # Create pygal graph
  octet_chart = pygal.Line()

  octet_chart.title = '%s Input/Output Octets' % ifdescr
  
  octet_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']

  octet_chart.add('InOctets', graph_list[0])
  octet_chart.add('OutOctets', graph_list[1])

  octet_chart.render_to_file('/home/pperreault/classwork/files/In_Out_Octets.svg')

  line_chart = pygal.Line()

  line_chart.title = '%s Input/Output Unicast Packets' % ifdescr

  line_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']

  line_chart.add('InUnicast', graph_list[2])
  line_chart.add('OutUnicast', graph_list[3])

  line_chart.render_to_file('/home/pperreault/classwork/files/In_Out_Ucast.svg')

def save_raw_data(device_a, ifdescr, ifinoctets, ifoutoctets, ifinucast, ifoutucast):

  # Create lists to store 
  in_oct = []
  out_oct = []
  in_ucast = []
  out_ucast = []

  file_name = "/home/pperreault/classwork/files/" + device_a[0] + "_" + ifdescr + ".pkl"
  
  # Check if file name exists and load lists if TRue
  if os.path.isfile(file_name):
    f = open(file_name, "rb")
    in_oct = pickle.load(f)
    out_oct = pickle.load(f)
    in_ucast = pickle.load(f)
    out_ucast = pickle.load(f)
    f.close()

  counter_list = in_oct, out_oct, in_ucast, out_ucast

  # Iterate over lists, if 13+ items, remove first (oldest)
  for counter in counter_list:  
    while len(counter) >= 13:
      del counter[:1]
  
  # Append current polled value 
  in_oct.append(ifinoctets)
  out_oct.append(ifoutoctets)
  in_ucast.append(ifinucast)
  out_ucast.append(ifoutucast)

  # Save data to pickle file
  f = open(file_name, "wb")
  for counter in counter_list:  
    pickle.dump(counter, f)

  f.close()

def main():

  # Define v3 variables
  auth_key = 'galileo1'
  encrypt_key = 'galileo1'
  user = 'pysnmp'

  # Define snmp user
  user_a = (user, auth_key, encrypt_key)

  # Define devices which will be tested
  device_a = ('50.242.94.227', '7961')
  #device_b = ('50.242.94.227', '8061')

  int_oid_dict = {
    'ifDescr_fa4': '1.3.6.1.2.1.2.2.1.2.5',
    'ifInOctets_fa4': '1.3.6.1.2.1.2.2.1.10.5',
    'ifOutOctets_fa4': '1.3.6.1.2.1.2.2.1.16.5',
    'ifInUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.11.5',
    'ifOutUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.17.5'
}
  
  # Poll for SNMP data
  ifdescr = snmp_extract(snmp_get_oid_v3(device_a, user_a, int_oid_dict['ifDescr_fa4']))
  ifinoctets = snmp_extract(snmp_get_oid_v3(device_a, user_a, int_oid_dict['ifInOctets_fa4']))
  ifoutoctets = snmp_extract(snmp_get_oid_v3(device_a, user_a, int_oid_dict['ifOutOctets_fa4']))
  ifinucast = snmp_extract(snmp_get_oid_v3(device_a, user_a, int_oid_dict['ifInUcastPkts_fa4']))
  ifoutucast = snmp_extract(snmp_get_oid_v3(device_a, user_a, int_oid_dict['ifOutUcastPkts_fa4']))

  # Save raw data to pickle file
  save_raw_data(device_a, ifdescr, ifinoctets, ifoutoctets, ifinucast, ifoutucast)

  # Graph data to .svg file 
  graph_data(device_a, ifdescr)

if __name__ == '__main__':

  main()
