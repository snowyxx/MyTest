#!/usr/bin/env python

import telnetlib
import threading
import os
import re
import sys

def do_telnet(host, username, password, finish, commands, linesep):
    tn = telnetlib.Telnet(host, port=23, timeout=10)
    # tn.set_debuglevel(2)

    tn.read_until('login : ')
    tn.write(username + linesep)

    tn.read_until('Password:')
    tn.write(password + linesep)

    tn.read_until(finish)
    output=''
    for command in commands:
        tn.write(command+linesep)
        output+=tn.read_until(finish)
    tn.close()
    
    fans=re.findall(r'(Fan.*?)\s{2,}(\d+%)',output)  
    volts=re.findall(r'Planar.*\n',output)
    temp=re.findall(r'(Ambient Temp)\s+.+?\s+.+?\s+.*?/(.*?)\s',output)
    power=re.findall(r'(Power\s+.*?)\s',output)
    state=re.findall(r'(State\s+.*?)(\r)?\n',output)
    restarts=re.findall(r'(Restarts\s+.*?)\s',output)
    
    print '<--table FAN starts-->'
    print 'Name@Speed'
    if fans:
        for fan in fans:
            print fan[0]+'@'+fan[1]
    print '<--table FAN ends-->'
    
    print '<--table VOLT starts-->'
    print 'Name@Volt'
    if volts:
        for volt in volts:
            columns=re.findall(r'(Planar.*?)(?:\s{2,}.+?){4}\s{2,}(.+?)\s',volt)
            if len(columns)>0:
                print columns[0][0]+'@'+columns[0][1]
    print '<--table VOLT ends-->'
    
    
    print '<--table TEMP starts-->'
    print 'Name@Temp'
    if temp:
        print temp[0][0]+'@'+temp[0][1]
    print '<--table TEMP ends-->'
    
    if power:
        print power[0].split()[0]+'='+power[0].split()[1]
    if state:
        print state[0][0].split()[0]+'='+state[0][0].split()[1]+' '+state[0][0].split()[2]
    if restarts:
        print restarts[0].split()[0]+'='+restarts[0].split()[1]
    
if __name__ == '__main__':
    host = '192.168.0.199'
    username = 'USERID'
    password = 'PASSW0RD'
    if len(sys.argv)>3:
        host=sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
    finish = 'system>'
    linesep = os.linesep
    commands = ['fans','volts','temps','syshealth']
    # do_telnet(host, username, password, finish, commands)
    th1 = threading.Thread(target=do_telnet, args=(host, username, password, finish, commands,linesep))
    th1.start()
    th1.join(20)
    