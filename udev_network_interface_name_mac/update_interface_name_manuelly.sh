#!/bin/bash
if [ $# -ne 2 ]; then
        echo ****Usage:*******
        echo $0 ethX Mac
else
        ruleFile="/etc/udev/rules.d/70-persistent-net.rules"
        if [ -e ${ruleFile}_0 ]; then
                 cp -f ${ruleFile} ${ruleFile}_last
        else
                cp ${ruleFile} ${ruleFile}_0
        fi
        interfaceName=$1
        macAddress=$2
        sed -i ''/${interfaceName}/{s@\\\(ATTR{address}==\"\\\)[^\"]\\+@\\1${macAddress}@}''  ${ruleFile}
fi