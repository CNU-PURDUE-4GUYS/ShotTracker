#!/bin/bash

#while true; do

######### Phase #1 : Target Setting
#targetNumber=`python3 receiveTargetNumber.py` # via BT
targetNumber=1
echo "$targetNumber"	#	format: b'#'
var_ACK=`./sendTargetNumber sender $targetNumber` # via LoRa
#echo "$var_ACK"

# if ACK received, then give ACK to Android
#./sendTargetNumber | while read line; do
if [ "$var_ACK" = "ACK" ];
then 
	echo "HO!"
	#python3 giveACK.py  # via BT
fi
