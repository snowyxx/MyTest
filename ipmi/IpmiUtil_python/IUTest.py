#!/usr/bin/evn python

import re
import subprocess
import sys

def runCMDBySubProcess(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    # print output
    # print p_status
    return (p_status, output)


def main(host, user, passwd):
    sensorCmd = 'ipmiutil sensor  -N '+host+' -U '+user+' -P '+passwd+' -s'
    healthCmd = 'ipmiutil health  -N '+host+' -U '+user+' -P '+passwd

    tables = {}  # {"fan":[[sNum,Name,Status,Reading],[sNum,Name,Status,Reading]]}
    
    sensorOutput = runCMDBySubProcess(sensorCmd)
    if sensorOutput[0] == 0:
        sensorResult = sensorOutput[1]
        for line in sensorResult.split('\n'):
            if line.find('|') > -1:
                columns=[x.strip() for x in line.split('|')]
                if '' in columns:
                    columns[columns.index('')]='-'
                tableName = columns[2]
                value = columns[3:]
                tables.setdefault(tableName, []).append(value)
                
    for tabName, tabValues in tables.items():
        if tabName is 'Type':
            continue
        print '<--table {} starts-->'.format(tabName)
        print 'index|sNum|Name|Status|Reading'
        for idx, row in enumerate(tabValues):
            print '{}|{}'.format(idx,'|'.join(row))
        print '<--table {} ends-->'.format(tabName)

    healthOutput = runCMDBySubProcess(healthCmd)
    if healthOutput[0] == 0:
        healthResult = healthOutput[1]
        for line in healthResult.split('\n'):
            ipmiutilVer_M = re.search(r'(ipmiutil ver)\s+(.*)', line)
            bmcVer_M = re.search(
                r'BMC version\s*?=\s*?(.*?),\s*?IPMI\s*?v(.*)', line)
            bmcVendor_M = re.search(
                r'BMC manufacturer.*\((.*?)\).*?\((.*?)\)', line)
            powerStat_M = re.search(r'Power State.*\((.*?)\)', line)
            if ipmiutilVer_M:
                print ipmiutilVer_M.group(1)+'='+ipmiutilVer_M.group(2)
            elif bmcVendor_M:
                print "BMC manufacturer="+bmcVendor_M.group(1)+"-"+bmcVendor_M.group(2)
            elif bmcVer_M:
                print 'BMC version='+bmcVer_M.group(1)
                print 'IPMI version='+bmcVer_M.group(2)
            elif powerStat_M:
                print 'Power State='+powerStat_M.group(1)
if __name__ == '__main__':
    if len(sys.argv) > 3:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        main(host, user, passwd)


'''
yantekiMacBook-Pro:Downloads yan$ ipmiutil sensor  -N 192.168.0.19 -U USERID -P PASSW0RD
ipmiutil ver 2.95
isensor: version 2.95
Connecting to node 192.168.0.19 192.168.0.19
-- BMC version 1.25, IPMI version 2.0
 ID  | SDRType | Type            |SNum| Name             |Status| Reading
0001 | Full    | Temperature     | 32 | Ambient Temp     | OK   | 26.00 C
0002 | Full    | FRU Sensor      | 33 | Altitude         | OK   | 0.00 ft
0003 | Full    | Current         | 2e | Avg Power        | OK   | 170.00 W
0004 | Full    | Voltage         | 16 | Planar 3.3V      | OK   | 3.28 V
0005 | Full    | Voltage         | 17 | Planar 5V        | OK   | 4.93 V
0006 | Full    | Voltage         | 18 | Planar 12V       | OK   | 11.93 V
0007 | Full    | Voltage         | 1c | Planar VBAT      | OK   | 2.98 V
0008 | Full    | Fan             | 40 | Fan 1A Tach      | OK   | 2929.00 RPM
0009 | Full    | Fan             | 41 | Fan 1B Tach      | OK   | 2100.00 RPM
000a | Full    | Fan             | 42 | Fan 2A Tach      | OK   | 2088.00 RPM
000b | Full    | Fan             | 43 | Fan 2B Tach      | OK   | 1700.00 RPM
000c | Full    | Fan             | 44 | Fan 3A Tach      | OK   | 3045.00 RPM
000d | Full    | Fan             | 45 | Fan 3B Tach      | OK   | 2375.00 RPM
000e | Compact | Entity Presence | 50 | Fan 1            | OK*  |
000f | Compact | Entity Presence | 51 | Fan 2            | OK*  |
0010 | Compact | Entity Presence | 52 | Fan 3            | OK*  |
0011 | Compact | Entity Presence | 83 | Front Panel      | OK*  |
0012 | Compact | Cable/Interconn | 84 | Video USB        |  _  |
0013 | Compact | Entity Presence | 85 | DASD Backplane 1 | OK*  |
0014 | Compact | Entity Presence | 82 | SAS Riser        | OK*  |
0015 | Compact | Entity Presence | 89 | PCI Riser 1      | OK*  |
0016 | Compact | Entity Presence | 8a | PCI Riser 2      | OK*  |
0017 | Compact | Processor       | 90 | CPU 1            | ProcPresent |
0018 | Compact | Processor       | 91 | CPU 2            | ProcPresent |
0019 | Compact | Processor       | 93 | All CPUs         | OK   |
001a | Compact | Processor       | 94 | One of The CPUs  | OK   |
001b | Compact | Temperature     | 31 | IOH Temp Status  | OK   |
001c | Compact | Temperature     | c0 | CPU 1 OverTemp   | OK   |
001d | Compact | Temperature     | c1 | CPU 2 OverTemp   | OK   |
001e | Compact | System Event    | cb | CPU Fault Reboot | OK   |
001f | Compact | System Event    | cc | Aux Log          | OK   |
0020 | Compact | Critical Interr | 80 | NMI State        | OK   |
0021 | Compact | System Firmware | 92 | ABR Status       |  _  |
0022 | Compact | System Firmware | b4 | Firmware Error   |  _  |
0023 | Compact | Critical Interr | b0 | PCIs             | OK   |
0024 | Compact | Critical Interr | b1 | CPUs             | OK   |
0025 | Compact | Critical Interr | b2 | DIMMs            | OK   |
0026 | Compact | Chip Set        | b3 | Sys Board Fault  |  _  |
0027 | Compact | Power Supply    | 70 | Power Supply 1   | Present |
0028 | Compact | Power Supply    | 71 | Power Supply 2   | NotAvailable |
0029 | Compact | Fan             | 73 | PS 1 Fan Fault   | Ready |
002a | Compact | Fan             | 74 | PS 2 Fan Fault   | Ready |
002b | Compact | Power Supply    | 28 | VT Fault         | Absent |
002c | Compact | Current         | 29 | Pwr Rail A Fault |  _  |
002d | Compact | Current         | 2a | Pwr Rail B Fault |  _  |
002e | Compact | Current         | 2b | Pwr Rail C Fault |  _  |
002f | Compact | Current         | 2c | Pwr Rail D Fault |  _  |
0030 | Compact | Current         | 2d | Pwr Rail E Fault |  _  |
0031 | Compact | Power Supply    | 75 | PS 1 Therm Fault | Present |
0032 | Compact | Power Supply    | f5 | PS 1 OP Fault    | Present |
0033 | Compact | Power Supply    | f6 | PS 2 OP Fault    | Present |
0034 | Compact | Power Supply    | 76 | PS 2 Therm Fault | Present |
0035 | Compact | Power Supply    | 77 | PS1 12V OV Fault | Present |
0036 | Compact | Power Supply    | 78 | PS2 12V OV Fault | Present |
0037 | Compact | Power Supply    | 79 | PS1 12V UV Fault | Present |
0038 | Compact | Power Supply    | 7a | PS2 12V UV Fault | Present |
0039 | Compact | Power Supply    | 7b | PS1 12V OC Fault | Present |
003a | Compact | Power Supply    | 7c | PS2 12V OC Fault | Present |
003b | Compact | Power Supply    | 7d | PS 1 VCO Fault   | Present |
003c | Compact | Power Supply    | 7e | PS 2 VCO Fault   | Present |
003d | Compact | Power Supply    | 7f | Power Unit       | Absent |
003e | Compact | Cooling Device  | 5c | Cooling Zone 1   |  _  |
003f | Compact | Cooling Device  | 5d | Cooling Zone 2   |  _  |
0040 | Compact | Cooling Device  | 5e | Cooling Zone 3   |  _  |
0041 | Compact | Drive Slot      | 60 | Drive 0          | Unused   Faulty |
0042 | Compact | Drive Slot      | 61 | Drive 1          | Unused   Faulty |
0043 | Compact | Drive Slot      | 62 | Drive 2          | Unused   |
0044 | Compact | Drive Slot      | 63 | Drive 3          | Unused   |
0045 | Compact | Drive Slot      | 64 | Drive 4          | Unused   |
0046 | Compact | Drive Slot      | 65 | Drive 5          | Unused   |
0047 | Compact | Drive Slot      | 66 | Drive 6          | Unused   |
0048 | Compact | Drive Slot      | 67 | Drive 7          | Unused   |
0049 | Compact | Drive Slot      | 68 | Drive 8          | Unused   |
004a | Compact | Drive Slot      | 69 | Drive 9          | Unused   |
004b | Compact | Drive Slot      | 6a | Drive 10         | Unused   |
004c | Compact | Drive Slot      | 6b | Drive 11         | Unused   |
004d | Compact | Drive Slot      | 6c | Drive 12         | Unused   |
004e | Compact | Drive Slot      | 6d | Drive 13         | Unused   |
004f | Compact | Drive Slot      | 6e | Drive 14         | Unused   |
0050 | Compact | Drive Slot      | 6f | Drive 15         | Unused   |
0051 | Compact | Memory          | 34 | All DIMMS        | OK   |
0052 | Compact | Memory          | 35 | One of the DIMMs | OK   |
0053 | Compact | Memory          | d0 | DIMM 1           | OK   |
0054 | Compact | Memory          | d1 | DIMM 2           | OK   |
0055 | Compact | Memory          | d2 | DIMM 3           | OK   |
0056 | Compact | Memory          | d3 | DIMM 4           | OK   |
0057 | Compact | Memory          | d4 | DIMM 5           | OK   |
0058 | Compact | Memory          | d5 | DIMM 6           | OK   |
0059 | Compact | Memory          | d6 | DIMM 7           | OK   |
005a | Compact | Memory          | d7 | DIMM 8           | OK   |
005b | Compact | Memory          | d8 | DIMM 9           | OK   |
005c | Compact | Memory          | d9 | DIMM 10          | OK   |
005d | Compact | Memory          | da | DIMM 11          | OK   |
005e | Compact | Memory          | db | DIMM 12          | OK   |
005f | Compact | Memory          | dc | DIMM 13          | OK   |
0060 | Compact | Memory          | dd | DIMM 14          | OK   |
0061 | Compact | Memory          | de | DIMM 15          | OK   |
0062 | Compact | Memory          | df | DIMM 16          | OK   |
0063 | Compact | Memory          | f1 | DIMM 17          | OK   |
0064 | Compact | Memory          | f2 | DIMM 18          | OK   |
0065 | Compact | Temperature     | e0 | DIMM 1 Temp      | OK*  |
0066 | Compact | Temperature     | e1 | DIMM 2 Temp      | OK   |
0067 | Compact | Temperature     | e2 | DIMM 3 Temp      | OK   |
0068 | Compact | Temperature     | e3 | DIMM 4 Temp      | OK*  |
0069 | Compact | Temperature     | e4 | DIMM 5 Temp      | OK*  |
006a | Compact | Temperature     | e5 | DIMM 6 Temp      | OK   |
006b | Compact | Temperature     | e6 | DIMM 7 Temp      | OK*  |
006c | Compact | Temperature     | e7 | DIMM 8 Temp      | OK*  |
006d | Compact | Temperature     | e8 | DIMM 9 Temp      | OK   |
006e | Compact | Temperature     | e9 | DIMM 10 Temp     | OK*  |
006f | Compact | Temperature     | ea | DIMM 11 Temp     | OK   |
0070 | Compact | Temperature     | eb | DIMM 12 Temp     | OK   |
0071 | Compact | Temperature     | ec | DIMM 13 Temp     | OK*  |
0072 | Compact | Temperature     | ed | DIMM 14 Temp     | OK*  |
0073 | Compact | Temperature     | ee | DIMM 15 Temp     | OK   |
0074 | Compact | Temperature     | ef | DIMM 16 Temp     | OK*  |
0075 | Compact | Temperature     | f3 | DIMM 17 Temp     | OK*  |
0076 | Compact | Temperature     | f4 | DIMM 18 Temp     | OK   |
0077 | Compact | OS Critical Sto | c4 | PCI 1            | Absent |
0078 | Compact | OS Critical Sto | c5 | PCI 2            | Absent |
0079 | Compact | OS Critical Sto | c6 | PCI 3            | Absent |
007a | Compact | OS Critical Sto | c7 | PCI 4            | Absent |
007b | Compact | OS Critical Sto | c3 | All PCI Error    | Absent |
007c | Compact | OS Critical Sto | c9 | One of PCI Error | Absent |
007d | Compact | Watchdog_2      | 03 | IPMI Watchdog    | OK   |
007e | Compact | Power Unit      | 01 | Host Power       | Enabled  |
00ca | Compact | Entity Presence | 86 | DASD Backplane 2 | Present |
00cb | Compact | Entity Presence | 87 | DASD Backplane 3 | Absent |
00cc | Compact | Entity Presence | 88 | DASD Backplane 4 | Absent |
00ce | Compact | Memory          | 36 | Backup Memory    | OK   |
00cf | Compact | System Firmware | b5 | Progress         |  _  |
00e2 | Compact | Voltage         | f0 | Planar Fault     | Exceeded |
00e3 | Compact | Event Log       | b6 | SEL Fullness     | OK   |
00e4 | Compact | OS Critical Sto | c8 | PCI 5            | Absent |
00e5 | Compact | System Event    | 39 | OS RealTime Mod  | OK   |
ipmiutil sensor, completed successfully

yantekiMacBook-Pro:IUTest yan$ ipmiutil health  -N 192.168.0.19 -U USERID -P PASSW0RD
ipmiutil ver 2.95
ihealth ver 2.95
Connecting to node 192.168.0.19 192.168.0.19
BMC manufacturer  = 000002 (IBM), product = 00dc (x3650)
BMC version       = 1.25, IPMI v2.0
IPMI driver type  = 6        (lan)
Power State       = 00       (S0: working)
Selftest status   = 0055     (OK)
Chassis Status    = 21 00 00 00 (on, see below)
    chassis_power       = on
    pwr_restore_policy  = last_state
    chassis_intrusion   = inactive
    front_panel_lockout = inactive
    drive_fault         = false
    cooling_fan_fault   = false
Power On Hours    = 0 hours (0 days)
BMC LAN Channels  = 1
Chan 1 AuthTypes  = MD2 MD5 Straight_Passwd
ipmiutil health, completed successfully
'''
