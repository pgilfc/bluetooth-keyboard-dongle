#!/bin/bash

#Make sure the device has been removed and bluetoothctl is scanning

coproc bluetoothctl
echo -e "agent on" >&${COPROC[1]}
echo -e "default-agent" >&${COPROC[1]}
echo -e "trust $1\n" >&${COPROC[1]}
sleep 1
echo -e "pair $1\n" >&${COPROC[1]}
sleep 1
while bluetoothctl info $1 | grep "Connected: yes" ; do
    sleep 1
done
echo -e "connect $1\n" >&${COPROC[1]}
sleep 1
while bluetoothctl info $1 | grep "Connected: no" ; do
    sleep 1
done
echo -e "exit\n" >&${COPROC[1]}
