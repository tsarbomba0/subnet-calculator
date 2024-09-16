import math
import re

# variables for ip and number of hosts
# TODO: Make a input system for this
ip = [192, 168, 0, 2]
hosts = [511, 24, 12, 2]

# uses a logarithm to calculate the nearest power of 2 to generate a mask (except for 2)
def calculateMask(n):
    if n == 2:
        return 30
    else:
        return 32-math.ceil(math.log(n+2, 2))

# creates wildcard using mask
def generateWildcard(mask, i=0, output=""):
    while i<mask:
        output = output + "0"
        i+=1
    while len(output)<32:
        output = output + "1"
    output = re.findall("........", output)
    i=0
    for part in output:
        output[i] = int(output[i], 2)
        i+=1
    return output

# dec -> bin
def convertBinary(numarray, i=0):
    for part in numarray:
        numarray[i] = bin(numarray[i])[2:]
        if len(numarray[i]) != 8:
            a=0
            string=""
            while a<8-len(numarray[i]):
                string = string + "0"
                a += 1
            numarray[i] = string + numarray[i]
        i+=1
    return numarray

# bin -> dec
def convertDecimal(numarray, i=0):
    for part in numarray:
        numarray[i] = int(numarray[i], 2)
        i+=1
    return numarray

# combines the network address and wildcard to obtain a broadcast address
def combine(address, wildcard):
    i=0
    for part in address:
        #print(wildcard)
        #print(address)
        address[i] = address[i] + wildcard[i] 
        i+=1
    return address

# convert any address to the network address (requires mask)
def networkAddress(address, mask, i=0):
    tmp = convertBinary(address)
    binary_ip=""
    for part in tmp:
        binary_ip += tmp[i]
        i+=1
    i=0
    temp=""
    while i<32-mask:
        temp += "0"
        i+=1
    binary_ip = binary_ip[:-int((32-mask))] 
    binary_ip += temp
    output = re.findall("........", binary_ip)
    return convertDecimal(output)

# variables 
mask1 = calculateMask(hosts[0])
wildcard = generateWildcard(mask1)
network_address = networkAddress(ip, mask1)


# function to calculate the subnets
def calculateAll(hosts_num, addr, counter=0):
    # calculate mask
    mask = calculateMask(hosts_num)

    # TODO: Get this shit organised!
    if addr[3] >= 255:
        leftover = addr[3] - 255
        addr[3] = leftover
        addr[2] += 1
        if addr[2] >= 255:
            leftover = addr[2] - 255
            addr[2] = leftover
            addr[1] += 1
            if addr[1] >= 255:
                leftover = addr[1] - 255
                addr[1] = leftover
                addr[0] += 1
        net_addr = networkAddress(addr, mask)
    else:
        i=0
        for part in addr:
            addr[i] = int(addr[i])
            i += 1
        net_addr = addr
    wildcard = generateWildcard(mask)
    ######################################


    # convert all str to int
    i=0
    for part in addr:
        addr[i] = int(addr[i])
        i += 1
    
    # remove overflows from octets
    new_addr = combine(net_addr, wildcard)
    if new_addr[3] >= 255:
        leftover = addr[3] - 255
        new_addr[3] = leftover
        new_addr[2] += 1
        if new_addr[2] >= 255:
            leftover = addr[2] - 255
            new_addr[2] = leftover
            new_addr[1] += 1
            if new_addr[1] >= 255:
                leftover = addr[1] - 255
                new_addr[1] = leftover
                new_addr[0] += 1

    # debug info
    print(f'Counter: {counter} Mask: {mask} Wildcard: {wildcard} Netaddr: {net_addr} hostnum: {hosts[counter]} newaddr: {new_addr}')

    # counter, if counter exceeds the amount of host options, ends function
    counter = counter + 1
    if counter > len(hosts)-1:
        return 0
    
    # recursive function
    calculateAll(hosts[counter], new_addr, counter)

# running the function
calculateAll(hosts[0], network_address)