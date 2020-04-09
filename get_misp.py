import os
import argparse
import ipaddress
import subprocess
import time

from pymisp import ExpandedPyMISP
from keys import misp_url, misp_key

def get_all_misp():
    """
    Retrieve all misp events
    """
    return parse_misp(ExpandedPyMISP(misp_url, misp_key))

def parse_misp(misp):
    """
    Run command against misp server to obtain events
    """
    misp_parsed = misp.search()
    
    for i in misp_parsed:
        event_list = i['Event']['Attribute']
        for a in event_list:
            if a['to_ids']:
                try:
                    
                    ipversion = ipaddress.ip_address(a['value'])
                    if ipversion.version == 4:
                        check_iptables(str(ipversion))
                except:
                    pass

def check_iptables(ipadd):
    """
    check if ip exists in iptables to prevent duplicats
    """
    # tablecommand = subprocess.Popen(('/usr/bin/sudo', '/usr/bin/iptables', '-L', 'INPUT', '-v', '-n'), stdout=subprocess.PIPE)
    # tablecommand = subprocess.Popen(('/usr/bin/iptables', '-L', 'INPUT', '-v', '-n'), stdout=subprocess.PIPE)

    
    try:
        output = subprocess.check_output('/usr/bin/iptables -L INPUT -v -n | grep ' + ipadd, shell=True)

        
        # output = subprocess.check_output(('grep', ipadd), stdin=tablecommand.stdout)
        if output:
            print(ipadd + " already exists!")
    except:
        push_iptables(ipadd)

def push_iptables(ipadd):
    """
    push the items to iptables
    """

    # tablecommand = subprocess.call(['/usr/bin/sudo', '/usr/bin/iptables', '-A', 'INPUT', '-s', ipadd, '-j', 'DROP'], shell=True)
    # tablecommand = subprocess.call(['/usr/bin/iptables', '-A', 'INPUT', '-s', ipadd, '-j', 'DROP'], shell=True)
    tablecommand = subprocess.call('/usr/bin/iptables -A INPUT -s ' + ipadd + ' -j DROP', shell=True)

    if tablecommand == 0:
        print('Successfully added '+ ipadd)
    else:
        print('Something went wrong with the ipaddresses')
    
if __name__ == "__main__":
    get_all_misp()
