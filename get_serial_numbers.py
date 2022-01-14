from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
import traceback
from getpass import getpass
import logging
import time



def get_serial(connection):
    try: 
        hostname = connection.send_command('show version | in uptime').split()[0]
    except IndexError as err:
        hostname = "NOHOSTNAME"
    if (len(connection.send_command('show ver | include System serial number')) > 0):
        tmp_serial = (connection.send_command('show ver | include System serial number').split()[-1])
    elif (len(connection.send_command('show ver | include System Serial Number')) > 0):
        tmp_serial = (connection.send_command('show ver | include System Serial Number').split()[-1])
    elif (len(connection.send_command('show ver | include Top Assembly Serial Number')) > 0):
        tmp_serial = (connection.send_command('show ver | include Top Assembly Serial Number').split()[-1])
    elif (len(connection.send_command('show ver | include Processor board ID')) > 0):
        tmp_serial = (connection.send_command('show ver | include Processor board ID').split()[-1])
    elif (len(connection.send_command('show ver | include \*')) > 0):
        tmp_serial = (connection.send_command('show ver | include \*').split()[-1])
    else:
         tmp_serial = f"{hostname} is of an unusual type. Please check manually."
    return tmp_serial


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
            'ip': IP,
            'username': 'salernoda',
            'password': 'Ilike4sleep!',
            #'secret': switch_secret,
        }
        try:
            print(f"Gathering information on {Switch['ip']}")
            net_connect = ConnectHandler(**Switch)
            # fastest and easiest way to get the hostname, as far as I can tell
            try: 
                hostname = net_connect.send_command('show version | in uptime').split()[0]
            except IndexError as err:
                hostname = "NOHOSTNAME"
            serial_raw = get_serial(net_connect)
            
            # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
            serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'
            log_serials = open(serials_filename, "a")
            log_serials.write(hostname + "  " + Switch['ip'] + "  " + serial_raw + "\n")                   
            net_connect.disconnect()

        # If the IP is wrong or unreachable, we handle the timeout:
        except NetmikoTimeoutException as err:
            # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
            serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'
            log_serials = open(serials_filename, "a")
            log_serials.write(Switch['ip'] + " connection timed out! Check the IP address.\n")                       
            pass
        
        # If we fudged our credentials or SSH is not available on the device (or slow to authenticate)
      
        except NetmikoAuthenticationException as autherr:
            try:
                net_connect = ConnectHandler(**Switch)
                # fastest and easiest way to get the hostname, as far as I can tell
                try: 
                    hostname = net_connect.send_command('show version | in uptime').split()[0]
                except IndexError as err:
                    hostname = "NOHOSTNAME"       
                serial_raw = get_serial(net_connect)            
                # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
                serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'
                log_serials = open(serials_filename, "a")
                log_serials.write(hostname + "  " + Switch['ip'] + "  " + serial_raw + "\n")                       
                net_connect.disconnect()
            
                            
            except NetmikoAuthenticationException as autherr:
                try:
                    net_connect = ConnectHandler(**Switch)
                    # fastest and easiest way to get the hostname, as far as I can tell
                    try: 
                        hostname = net_connect.send_command('show version | in uptime').split()[0]
                    except IndexError as err:
                        hostname = "NOHOSTNAME"           
                    serial_raw = get_serial(net_connect)           
                    # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
                    serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'
                    log_serials = open(serials_filename, "a")
                    log_serials.write(hostname + "  " + Switch['ip'] + "  " + serial_raw + "\n")                       
                    net_connect.disconnect()
                
                except NetmikoAuthenticationException as autherr:    
                    # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
                    serials_filename = 'C://Users/salernoda/Documents/configs/serials/serials.txt'
                    log_serials = open(serials_filename, "a")
                    log_serials.write(Switch['ip'] + " had an authentication error\n")                       
                    pass
    

    
    



    