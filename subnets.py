import math
import re

# variables for ip and number of hosts
# TODO: Make a input system for this
ip = [192, 168, 0, 2]
hosts = [511, 255, 122, 24, 12, 2]

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

# function to -1 the address
def minusOneAddress(address):
    if address[3] == 0:
        address[3] = 255
        address[2] -= 1
    else:
        address[3] = address[3] - 1
    return address


# variables 
mask1 = calculateMask(hosts[0])
wildcard = generateWildcard(mask1)
network_address1 = networkAddress(ip, mask1)

result_to_return = []
# function to calculate the subnets
def calculateAll(hosts_num, addr, counter=0, output=""):
    ms = calculateMask(hosts_num)
    wildcard = generateWildcard(ms)
    network_address = combine(addr, wildcard)
    
    
    if network_address[3] > 254:
        network_address[3] = 0
        network_address[2] += 1
    for part in network_address:
        output = output + str(part) + "."
    
    result_to_return.append(output[:-1])

    counter += 1
    if counter == len(hosts):
        print(result_to_return)
        return result_to_return
    calculateAll(hosts[counter], network_address, counter)

# running the function
a = calculateAll(hosts[0], network_address1)
print(a)