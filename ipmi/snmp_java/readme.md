### Descripton

A script to get IMM monitor information by SNMP. 

### Monitored data

Default:

- TMP
- VOLT
- FAN
- Disk  (imm2 only)
- Power (imm2 only)
- CPU  (imm2 only)
- Memory
- Power Status
- System Status

Custome:

- Last 5 error log
- others

### Files

`imm.mib` and `immalert.mib` : IMM mib files of IMM2

`imm_1.mib` : IMM mib files of IMM v1

### oids.properties

- add your custome oids 
    - table oid name must start with TABLE_  e.g. #TABLE_Error=.1.3.6.1.4.1.2.3.51.3.2.1.1
    - single item oid name must start with ATTRI_    e.g #ATTRI_Power\ Status=.1.3.6.1.4.1.2.3.51.3.5.1.1.0
- snmp.debug.mode=true Debug mode : set this to log snmp api debug info. only "true" means enable the log
- snmpGetTableByMib = false  : Only set to "true" to get a table data by snmpGetAllList() base on a mib file, otherwise will try to use snmpGetNext()
- maxRowsNumber = 100  :Max rows to be got of a table oid, works when snmpGetTableByMib is not true

### Usage

`java -cp .;bin;lib\* IpmiSnmpTest <IP or host name> <snmp community>`
