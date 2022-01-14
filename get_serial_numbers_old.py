from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
import traceback
from getpass import getpass
import logging
import time

#switch_user = getpass(prompt='username: ')
#switch_password = getpass()
#switch_secret = getpass(prompt='enable secret: ')

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
# the default name for the input file is devices.txt
with open('devices.txt') as switches:
    for IP in switches:
        Switch = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': 'salernoda',
            'password': 'Ilike4sleep!',
            #'secret': switch_secret,
        }
        try:
            net_connect = ConnectHandler(**Switch)
            #time.sleep(1)
            # fastest and easiest way to get the hostname, as far as I can tell
            hostname = net_connect.send_command('show version | in uptime').split()[0]
            #time.sleep(1)
            serial_raw = net_connect.send_command('show ver | include \*')
            print (serial_raw)
            try:
                    serial_number = serial_raw.split()[-1]
            except IndexError as indie:
                serial_number = "111111111111111111111"
                print(indie)
                pass
            #serial_number = serial_raw.split()[-1]
            
            # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
            serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'

            log_serials = open(serials_filename, "a")
            year_code = serial_number[3:5]
            print(f"year_code: {year_code}")
            manufacture_year = str((int(year_code) + 1996))
            print(f"manufacturer_year: {manufacture_year}")
            log_serials.write(hostname + " " + serial_number + " " + manufacture_year + "\n")          
             
            net_connect.disconnect()

        # If the IP is wrong or unreachable, we handle the timeout:
        except NetmikoTimeoutException as err:
            failures_filename = 'C://Users/salernoda/Documents/configs/serials/failures.txt'

            log_failures = open(failures_filename, "a")
            log_failures.write(IP + "\n")
            print("There was a problem connecting via SSH")
            print(err)
            pass
        
        # If we fudged our credentials or SSH is not available on the device
      
        except NetmikoAuthenticationException as autherr:
            try:
                time.sleep(1)
                net_connect = ConnectHandler(**Switch)
                time.sleep(1)
                # fastest and easiest way to get the hostname, as far as I can tell
                hostname = net_connect.send_command('show version | in uptime').split()[0]
                time.sleep(1)
                serial_raw = net_connect.send_command('show ver | include \*')
                print (serial_raw)
                try:
                    serial_number = serial_raw.split()[-1]
                except IndexError as indie:
                    serial_number = "222222222222222222222222"
                    pass

            
                # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
                serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'

                log_serials = open(serials_filename, "a")
                year_code = serial_number[3:5]
                print(f"year_code: {year_code}")
                manufacture_year = str((int(year_code) + 1996))
                print(f"manufacturer_year: {manufacture_year}")
                log_serials.write(hostname + " " + serial_number + " " + manufacture_year + "\n")          
             
                net_connect.disconnect()

            
            except NetmikoAuthenticationException as autherr:
                auth_failures_filename = 'C://Users/salernoda/Documents/configs/serials/auth_failures.txt'

                log_auth_failures = open(auth_failures_filename, "a")
                log_auth_failures.write(IP + "\n")
                print(f"Authentication Error: {autherr}")
                #print("There was a problem authenticating to " + IP)
                #print("Make sure you used the correct login credentials and device allows SSH")
                #traceback.print_exc()
                #print("\n\n\n\n\n\n----------ERROR MESSAGE----------\n\n" + str(autherr) + "\n\n\n\n\n\n----------END ERROR MESSAGE----------\n\n")
                pass
def get_connected():
    

def get_serial(connection):
    hostname = connection.send_command('show version | in uptime').split()[0]
    
    if (len(connection.send_command('show ver | Show serial version')) > 0):
        tmp_serial = (connection.send_command('show ver | Show serial version').split()[-1])
    elif (len(connection.send_command('show ver | Show Serial Version')) > 0):
        tmp_serial = (connection.send_command('show ver | Show Serial Version').split()[-1])
    elif (len(connection.send_command('show ver | include \*')) > 0):
        tmp_serial = (connection.send_command('show ver | include \*').split()[-1])
    else:
         tmp_serial = "{hostname} is of an unusual type. Please check manually."
    return tmp_serial
    
    



    