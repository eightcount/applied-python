'''

Using SNMPv3 create a script that detects changes to the running configuration. 
If the running configuration is changed, then send an email notification to yourself 
identifying the router that changed and the time that it changed.

'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
import pickle
import os.path
from email.mime.text import MIMEText
import email_helper, smtplib

def send_mail(recipient, subject, body, sender):

  message = MIMEText(body)
  message['Subject'] = subject
  message['From'] = sender
  message['To'] = recipient

  # Create SMTP connetion object to localhost
  smtp_conn = smtplib.SMTP('localhost')

  # Send the email
  smtp_conn.sendmail(sender, recipient, message.as_string())

  # Close the SMTP connection
  smtp_conn.quit()
  
  return True

def process_data(current_time, dev):

  # Prime variable
  conf_change = False

  # Create unique file name to store data for each device in list
  file_name = "/home/pperreault/classwork/files/" + dev[0] + "_" + dev[1] + "_data.pkl"

  # Check if previous save data exists and save to variable if True
  if os.path.isfile(file_name): 
    f = open(file_name, "rb")
    previous_time = pickle.load(f)
    f.close()

    # True if a change has been made
    if int(previous_time) != int(current_time):
      conf_change = True      

    else:
      conf_change = False 

  # Write current data to pickle file
  f = open(file_name, "wb")
  pickle.dump(current_time, f)
  f.close()

  # Return true if configuration change has occured since last check
  if conf_change:
    return True 

  else:
    return False 

# Function to comapare run and start configs
def last_change_last_save(run_last_change, start_last_change):

  if start_last_change == 0:
    return False
    
  elif start_last_change >= run_last_change:
    return True
    
  return False

def main():

  # Define snmp user
  user_a = ('pysnmp', 'galileo1', 'galileo1')
  
  # Define devices which will be tested
  device_a = ('50.242.94.227', '7961')
  device_b = ('50.242.94.227', '8061')
  dev_list = device_a, device_b

  # System Uptime
  oidSysUptime = '1.3.6.1.2.1.1.3.0'
  # Uptime when running config last changed
  oidRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'
  # Uptime when running config last saved (note any 'write' constitutes a save)
  oidRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'
  # Uptime when startup config last saved
  oidStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'

  for dev in dev_list:
    # Gather data
    sys_uptime = snmp_extract(snmp_get_oid_v3(dev, user_a, oidSysUptime)) # sysUptime
    run_last_change = snmp_extract(snmp_get_oid_v3(dev, user_a, oidRunningLastChanged)) # sysUptime @ last running config change
    run_last_save = snmp_extract(snmp_get_oid_v3(dev, user_a, oidRunningLastSaved)) # sysUptime @ last "write" command
    start_last_change = snmp_extract(snmp_get_oid_v3(dev, user_a, oidStartupLastChanged)) # sysUptime @ last startup config change
    
    # Compare running and startup configs
    #change_save_state = last_change_last_save(run_last_change, start_last_change)
 
    # What do we want to do with this information?
    run_conf_change = process_data(run_last_change, dev)
 
    # Action to take if running configuration change detected
    if run_conf_change:
      
      # Define mail variables
      recipient = 'peter.perreault@gmail.com'
      sender = 'Someone@somewhere'
      subject = '[NOTIFY] Configuration Change'
      body = 'A running configuration change has been detected on device %s' % dev[0]
       
      send_mail(recipient, subject, body, sender)

if __name__ == '__main__':

  main()
