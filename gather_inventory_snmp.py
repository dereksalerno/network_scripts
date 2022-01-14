from pysnmp import hlapi
import sys
from pysnmp.hlapi import *
import socket


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port), timeout=.5, retries=0),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

def make_list():
    switch_list = []
    with open('devices.txt') as switches:
        for IP in switches:
            switch_list.append(IP.rstrip())
    return switch_list

def walk(host, oid):
    for (errorIndication,
        errorStatus,
        errorIndex,
        varBinds) in nextCmd(SnmpEngine(), 
                            CommunityData('city.network'), 
                            UdpTransportTarget((host, 161)), 
                            ContextData(),
                             ObjectType(ObjectIdentity(oid)), 
                             lexicographicMode=False):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                file=sys.stderr)             
            break
        else:
            for varBind in varBinds:
                print(str(varBind))
                #print(varBind)

switches = make_list()

for IP in switches:
    try:
        serials_filename = 'serials.txt'
        log_serials = open(serials_filename, "a")
        serial_snmp_code='1.3.6.1.4.1.9.3.6.3.0'
        hostname_snmp_code='1.3.6.1.2.1.1.5.0'
        stack_status='.1.3.6.1.4.1.9.9.500.1.2.1.1.7.1001'
        model_snmp_code='.1.3.6.1.4.1.9.9.25.1.1.1.2'
        #model_snmp_code='.1.3.6.1.2.1.1'
        boop = str(IP)      
        stacky = (get(IP, [stack_status], hlapi.CommunityData('city.network'))).get(stack_status)
        checked_stacky=""
        if (len(str(stacky)) < 1):
            pass
        else:
            checked_stacky=str(stacky)
        serial = (get(IP, [serial_snmp_code], hlapi.CommunityData('city.network'))).get(serial_snmp_code)
        hostname = (get(IP, [hostname_snmp_code], hlapi.CommunityData('city.network')).get(hostname_snmp_code)).removesuffix(".ci.richmond.va.us")
        log_serials.write(hostname + "  " + IP + " " + serial + " " + checked_stacky + "\n" )
        walk(IP, model_snmp_code)
        #print((get(IP, [model_snmp_code], hlapi.CommunityData('city.network'))).get(model_snmp_code))
    except RuntimeError:
        print('ignoring: ' + IP)
    except OSError:
        print("TTL exceeded on: " + IP)
        pass
    except socket.error:
        pass



   