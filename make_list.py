switches = []
with open('devices.txt') as source:
    for line in source:
        switches = list(map(str,line.split())) 

device_filename = 'device_list.txt'
log_devices = open(device_filename, "a")
log_devices.write("[")

for IP in switches:
    device_filename = 'device_list.txt'
    log_devices = open(device_filename, "a")
    log_devices.write('\'' + IP + '\', ')
log_devices.write("]")

