#!/bin/bash

PING=`ping -c 3 -s 1 192.168.199.220 | grep '0 received' | wc -l`

echo -en $PING

