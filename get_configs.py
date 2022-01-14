from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
from getpass import getpass
#from getpass import getuser

switch_user = getpass(prompt='username: ')
switch_password = getpass()
switch_secret = getpass(prompt='enable secret: ')


# the default name for the input file is devices.txt
with open('devices.txt') as switches:
    for IP in switches:
        Switch = {
            'device_type': 'cisco_ios',
            'ip': IP,
            'username': switch_user,
            'password': switch_password,
            'secret': switch_secret,
        }
        try:
            
            net_connect = ConnectHandler(**Switch)

            # fastest and easiest way to get the hostname, as far as I can tell
            hostname = net_connect.send_command('show version | in uptime').split()[0]
            
            # TODO: If someone else is using this script, specify the correct path!! Also, .ios extensions are simply for VSCode syntax highlighting
            details_filename = 'C://Users/salernoda/Documents/configs/details/' + hostname + '_details.txt.ios'
            config_filename = 'C://Users/salernoda/Documents/configs/showrun/' + hostname + '_showrun.txt.ios'

            try:
                net_connect.enable()
                showrun = net_connect.send_command('show run')
                
                #put the running config in a file by itself with no additional information
                log_showrun = open(config_filename, "a")
                log_showrun.write(showrun)
            
            # Incorrect enable passwords bring a ValueError, which we handle here
            except ValueError as valerr:
                print("Enable Password seems to be wrong for this switch: " + hostname + ".\n\n Skipping show run...\n")
                log_showrun = open(config_filename + "ERROR", "a")
                log_showrun.write("There was something wrong with the enable password")
                pass

            

                
            #Load up variables by sending commands to switch / router
            
            showver = net_connect.send_command('show version')
            intstat = net_connect.send_command('show interface status')
            cdpnei = net_connect.send_command('show cdp neighbor')
            cdpnei_detail = net_connect.send_command('show cdp neighbor detail')

            

            # details will be in a separate file delineated by newlines and labelled
            log_details = open(details_filename, "a")
            log_details.write("\n\n\n")
            log_details.write(" -------- show version --------")
            log_details.write("\n\n\n")
            log_details.write(showver)
            log_details.write("\n\n\n")

            log_details.write(" -------- show interface status --------")
            log_details.write("\n\n\n")
            log_details.write(intstat)
            log_details.write("\n\n\n")

            log_details.write(" -------- show cdp neighbor --------")
            log_details.write("\n\n\n")
            log_details.write(cdpnei)
            log_details.write("\n\n\n")


            log_details.write(" -------- show cdp neighbor detail --------")
            log_details.write("\n\n\n")
            log_details.write(cdpnei_detail)
            log_details.write("\n\n\n")

            #now that we have gotten what we need, let's close the connection
            net_connect.disconnect()

        # If the IP is wrong or unreachable, we handle the timeout:
        except NetmikoTimeoutException as err:
            print("There was a problem connecting via SSH")
            print(err)
            pass
        
        # If we fudged our credentials or SSH is not available on the device
        except NetmikoAuthenticationException as autherr:
            print("There was a problem authenticating to " + IP)
            print("Make sure you used the correct login credentials and device allows SSH")
            print("\n\n\n\n\n\n----------ERROR MESSAGE----------\n\n" + str(autherr) + "\n\n\n\n\n\n----------END ERROR MESSAGE----------\n\n")
            pass

    