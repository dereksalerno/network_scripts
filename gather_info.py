from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
import traceback
from getpass import getpass
import logging
import time
from datetime import date, datetime



def get_auth():
    creds = {}
    username = getpass(prompt="Username for SSH sign-in: ")
    pw = getpass(prompt="Password for SSH sign-in: ")
    creds = { "username": username, "password": pw}
    return creds

def get_model(connection):
    if (len(connection.send_command("show ver | include Model Number")) >0):
        model = (connection.send_command("show ver | include Model Number").split()[-1])
    elif (len(connection.send_command("show ver | include Model number")) >0):
        model = (connection.send_command("show ver | include Model number").split()[-1])
    else:
        model = "Mode Not Detected"
    return model

def get_hostname(connection):
    try:
        hostname = connection.find_prompt()[:-1]
    except IndexError as err:
        hostname = "NOHOSTNAME"
    return hostname

def get_serial(connection):
    if (len(connection.send_command("show ver | include \'System serial number\'")) > 0):
        tmp_serial = (connection.send_command("show ver | include \'System serial number\'").split()[-1])
    elif (len(connection.send_command("show ver | include \'System Serial Number\'")) > 0):
        tmp_serial = (connection.send_command("show ver | include \'System Serial Number\'").split()[-1])
    elif (len(connection.send_command("show ver | include \'Top Assembly Serial Number\'")) > 0):
        tmp_serial = (connection.send_command("show ver | include \'Top Assembly Serial Number\'").split()[-1])
    elif (len(connection.send_command("show ver | include \'Serial Number\'")) > 0):
        tmp_serial = (connection.send_command("show ver | include \'Serial Number\'").split()[-1])
    elif (len(connection.send_command("show ver | include \"Serial Number\"")) > 0):
        tmp_serial = (connection.send_command("show ver | include \"Serial Number\"").split()[-1])
    elif (len(connection.send_command("show ver | include \'Processor board ID\'")) > 0):
        tmp_serial = (connection.send_command("show ver | include \'Processor board ID\'").split()[-1])
    elif (len(connection.send_command("show ver | include Processor")) > 0):
        tmp_serial = (connection.send_command("show ver | include Processor").split()[-1])
    elif (len(connection.send_command("show ver | include \*")) > 0):
        tmp_serial = (connection.send_command("show ver | include \*").split()[-1])
    else:
        hostname=get_hostname(connection)
        tmp_serial = f"{hostname} is of an unusual type. Please check manually."
    return tmp_serial

def make_filename():
    now = datetime.now()
    current_time = now.strftime("%b-%d-%Y_%H:%M:%S")
    filename = ("Hardware_Inventory_" + current_time)
    return filename

def make_list():
    switch_list = []
    with open('devices.txt') as switches:
        for IP in switches:
            switch_list.append(IP.rstrip())
    return switch_list

authorization_credentials = get_auth()

