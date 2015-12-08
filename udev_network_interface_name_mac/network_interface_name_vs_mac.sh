#!/bin/bash

ruleFile="/etc/udev/rules.d/70-persistent-net.rules"
for ifcfgpath in `ls /sys/class/net |grep eth` ; do
#	echo ${ifcfgpath}
	dev=`echo ${ifcfgpath}`
	ethtype=`ethtool ${dev} | grep "FIBRE" |wc -l`
#	echo ${dev}
#	echo ${ethtype}
#	echo "/sys/class/net/${dev}/address"
	if [ $ethtype -lt 1 ]; then
		TmacStr="${TmacStr} "`cat /sys/class/net/${dev}/address`
	else
		FmacStr="${FmacStr} "`cat /sys/class/net/${dev}/address`
	fi
done

TmacArr=($TmacStr)
for((i=0;i<${#TmacArr[@]};i++))
do
        n=i
        min=${TmacArr[$i]}
        for((j=i+1;j<${#TmacArr[@]};j++))
        do
                if [[ "${TmacArr[$j]}" < "$min" ]]
                then
                        n=$j
                        min=${TmacArr[$j]}
                fi
        done
        t=${TmacArr[$n]}
        TmacArr[$n]=${TmacArr[$i]}
        TmacArr[$i]=$t
done
for((i=0;i<${#TmacArr[@]};i++))
do
#        echo "${TmacArr[$i]} "
	#sed -i ''/eth${i}/{s@\\\(ATTR{address}==\"\\\)[^\"]\\+@\\1${TmacArr[$i]}@}'' 70-persistent-net.rules
	sed -i ''/eth${i}/{s@\\\(ATTR{address}==\"\\\)[^\"]\\+@\\1${TmacArr[$i]}@}''  ${ruleFile}
	#echo $#
done

FmacArr=($FmacStr)
for((i=0;i<${#FmacArr[@]};i++))
do
        n=i
        min=${FmacArr[$i]}
        for((j=i+1;j<${#FmacArr[@]};j++))
        do
                if [[ "${FmacArr[$j]}" < "$min" ]]
                then
                        n=$j
                        min=${FmacArr[$j]}
                fi
        done
        t=${FmacArr[$n]}
        FmacArr[$n]=${FmacArr[$i]}
        FmacArr[$i]=$t
done
#t=${FmacArr[1]}
#FmacArr[1]=${FmacArr[2]}
#FmacArr[2]=$t
for((i=0;i<${#FmacArr[@]};i++))
do
#        echo "${FmacArr[$i]} "
	#sed -i ''/eth$(expr $i + 4)/{s@\\\(ATTR{address}==\"\\\)[^\"]\\+@\\1${FmacArr[$i]}@}'' 70-persistent-net.rules
	sed -i ''/eth$(expr $i + 4)/{s@\\\(ATTR{address}==\"\\\)[^\"]\\+@\\1${FmacArr[$i]}@}'' ${ruleFile}
done
/bin/jre/bin/java -cp apm.jar APMDeploy
update-rc.d apm defaults
sleep 3
echo "Reboot now..."
init 6
