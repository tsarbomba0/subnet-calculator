import math
import re

## input, regex checks if it's a valid ip address with a mask in CIDR notation
try: 
    input_result = re.findall(r"\d{1,3}\.{1}\d{1,3}\.{1}\d{1,3}\.{1}\d{1,3}\/{1}\d{1,2}", input("Enter the IP address you wish to use in CIDR notation (ex. 10.0.0.0/8): "))[0].split('/')
    if int(input_result[1]) >= 32:
        exit()
    ip = []
    # Saving first entry for later
    saved_ip=""
    for octet in input_result[0].split('.'):
        ip.append(int(octet))
        saved_ip += octet+"."
    saved_ip = saved_ip[:-1]
except:
    print("Wrong syntax!")
    exit()

try:
    number_of_hosts = int(input("Number of subnets you need: "))
    hosts = []
    while True:
        hosts.append(int(input("Enter the desired number of hosts in a subnet: ")))
        if len(hosts) == number_of_hosts:
            break
except:
    print("Number must be a integer!")
    exit()
    


    


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

# dec -> bin (list)
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

# bin -> dec (list)
def convertDecimal(numarray):
    for part in numarray:
        numarray[numarray.index(part)] = int(numarray[numarray.index(part)], 2)
    return numarray

# combines the network address and wildcard to obtain a broadcast address
def combine(address, wildcard):
    for n in range(0, 4):
        address[n] += wildcard[n]
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
    for part in address:
        address[address.index(part)] = int(address[address.index(part)])
    if address[3] == 0:
        address[3] = 255
        address[2] -= 1
    else:
        address[3] = address[3] - 1
    return address

# breaks up ip strings (ex. 172.16.0.1) into lists of integers (ex. [172, 16, 0 ,1])
def breakupIntoInt(string):
    array = []
    string = string.split(".")
    for part in string:
        array.append(int(part))
    return array

# variables 
result_to_return = []
output_ips=[]
output_masks=[]
        
# function to calculate the subnets
def calculateAll(hosts_num, addr, counter=0, output=""):

    # variables for mask, wildcard mask and network address
    ms = calculateMask(hosts_num)
    wildcard = generateWildcard(ms)
    network_address = combine(addr, wildcard)

    # makes up for some loss in calculations
    network_address[3] += 1 
    
    # removing overflows
    if network_address[3] > 254:
        network_address[3] = 0
        network_address[2] += 1

    # converting number array into string
    for part in network_address:
        output = output + str(part) + "."
    
    # appending results with cutting the last character (a extra dot)
    result_to_return.append(output[:-1])
    result_to_return.append(ms)

    # counter (ends the function when it deals with the last address, to not cause a error)
    counter += 1
    if counter == len(hosts):
        return 0
    
    # recursion
    calculateAll(hosts[counter], network_address, counter)

# running the function
calculateAll(hosts[0], networkAddress(ip, calculateMask(hosts[0])))

# appending masks and ips to separate lists
i=0
for part in result_to_return:
    if (i % 2) == 0:
        output_ips.append(part) # ip list
    else:
        output_masks.append(part) # mask list
    i+=1

# inserting the saved ip converted to a network address from earlier to the list of ips from the recursive function
network_address = ""
for octet in networkAddress(breakupIntoInt(saved_ip), calculateMask(hosts[0])):
    network_address += str(octet)+"."
network_address = network_address[:-1]
output_ips.insert(0, network_address)

# main function that handles the printing part
def __main__(i=0, count=0, a=0):
    # for loop to handle the ips
    for string in output_ips:

        # Broadcast
        output = ""
        for element in minusOneAddress(breakupIntoInt(result_to_return[i % len(result_to_return)])):
            temp = breakupIntoInt(result_to_return[i % len(result_to_return)])
            output = output + str(element) + "."
        output = output[:-1]

        # First usable address
        output_range_first = ""
        range_first = breakupIntoInt(output_ips[count])
        range_first[3] += 1
        for element in range_first:
            output_range_first = output_range_first + str(element) + "."
        output_range_first = output_range_first[:-1]

        # Last usable address
        output_range_last = ""
        range_last = minusOneAddress(breakupIntoInt(result_to_return[i % len(result_to_return)]))
        range_last[3] -= 1
        for element in range_last:
            output_range_last = output_range_last + str(element) + "."
        output_range_last = output_range_last[:-1]

        

        
        # printing
        print(f' Network address: {output_ips[count]} Broadcast: {output} Usable range: {output_range_first}-{output_range_last} Mask: {output_masks[count]} Hosts: {hosts[count]} Unused hosts: {2**(32-output_masks[count])-hosts[count]-2}' )

        # counters
        if i % 2 == 0:
          i+=1
        i+=1
        count += 1
        if count == len(output_ips)-1:
            return 0


__main__()