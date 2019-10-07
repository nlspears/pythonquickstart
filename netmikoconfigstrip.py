##imports python modules needed to work
from netmiko import ConnectHandler
import time, sys, getpass, paramiko

##selects the correct Netmiko class based upon the device_type.
## I then define a network device dictionary consisting of a device_type, ip, username, and password.
user = raw_input("Enter your SSH username: ")
pword = getpass.getpass()


device = {
    'device_type': 'cisco_ios',
    #'ip': '192.168.43.10',
    'username': user,
    'password': pword,
    #'secret':'password'
}

ipfile=open("iplist.txt") #This file contains a list of switch ip addresses.
#print ("Please doublecheck your configuration in the config file. Please stop and figure out what you're about to do...")
#device['username']=input("Enter your SSH username:  ")
#device['password']=getpass.getpass()
isefile=open("isefile.txt") #opening the config file with the changes you want to push
iseconfig=isefile.read() ##reads the config file
isefile.close() #closes the config file

for line in ipfile:
    device['ip']=line.strip()
    print("Connecting to Device " + line)
    net_connect = ConnectHandler(**device)
    time.sleep(2)
    print ("Checking Interface Configurations")
    intfilter = net_connect.send_command("sh run | i Gi.")
    striplist = intfilter.strip()
    intfaces = striplist.splitlines()
    for x in intfaces:
       intconfig = net_connect.send_command("sh run " + x + " | i dot1x")
       findise = intconfig.find("dot1x")
       if findise > 0:
           gigintconfig = net_connect.send_command(x,)
           #print(net_connect.find_prompt())
           print ("Applying Configuration to " + x)
           #iseoutput1 = net_connect.send_config_from_file(isefile)
           gigintconfig += net_connect.send_config_set(iseconfig)
           print(gigintconfig)
       else:
           print("Non-ISE interface")
