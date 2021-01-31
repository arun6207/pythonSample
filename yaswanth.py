#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function  # import print from python3: end=""
import time
import re
import pexpect  # sudo apt-get install python-pexpect
import subprocess
import random


# !!! make sure bluetoothd runs in --compat mode before executing this script !!!
def pair_with_pin(start_time, pin,
                  time_limit=60):  # int(time.time()), pin - \d{4}, time_limit - approximate pairing window time in seconds, it might take up to 2x (nested timeout conditions)
    "exectutes pairing with entered PIN on bluetooth adapter side"
    pairing_status = False
    try:
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'sspmode', '0'])

        # bluetoothctl
        child = pexpect.spawn('bluetoothctl')
        child.expect("#")
        child.sendline('agent off')  # might be unnecessary
        child.expect("unregistered")

        child.sendline('agent DisplayOnly')
        child.expect("Agent registered")
        child.sendline('pairable on')
        child.expect("pairable on succeeded")
        child.sendline('discoverable on')
        child.expect("discoverable on succeeded")
        child.sendline('default-agent')
        print('Please input PIN: ' + pin)

        # waiting for Phone to send a pairing request...
        child.expect('Enter PIN code:', timeout=time_limit)  # timeout <= PAIRING_TIME_LIMIT to keep some kind of logic
        while int(
                time.time()) < start_time + time_limit:  # allow multiple pairing attempts during pairing window
            child.sendline(pin)
            i = child.expect(['Paired: yes', 'Enter PIN code:'], timeout=time_limit)
            if i == 0:  # found 'Paired: yes' == successful pairing
                trust_mac = 'trust ' + re.search(r'(?:[0-9a-fA-F]:?){12}.+$', child.before).group(
                    0)  # extract MAC from last line, one with 'Paired: Yes'
                child.sendline(trust_mac)  # optionally add device to trusted
                child.expect('trust succeeded', timeout=10)
                pairing_status = True
                break
            # else: # i == 1
            # print('wrong PIN, retrying if time will allow')
    except pexpect.EOF:
        print('!!!!!!!! EOF')
    except pexpect.TIMEOUT:
        print('!!!!!!!! TIMEOUT')

    # hide Pi's bluetooth for security reasons
    child.sendline('pairable off')
    child.expect("pairable off succeeded")
    child.sendline('discoverable off')
    child.expect("discoverable off succeeded")
    child.close()

    return pairing_status


# main program body
PAIRING_TIME_LIMIT = 60
BT_PIN = random.randint(1000, 10000)  # generate random 4-digit PIN 1000..9999

status = pair_with_pin(int(time.time()), str(BT_PIN), PAIRING_TIME_LIMIT)
if status == True:
    print('Pairing successful')