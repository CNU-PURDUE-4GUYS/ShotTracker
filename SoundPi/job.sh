#!/bin/bash

######### Phase #1 : Target Setting
targetNumber=`python3 receiveTargetNumber.py` # via BT
echo "$targetNumber"	#	format: b'#'
var_ACK=`./sendTargetNumber sender $targetNumber` # via LoRa

# if ACK received, then give ACK to Android
if [ "$var_ACK" = "ACK" ];
then 
	echo "ACK received!"
fi

######### Phase #2 : Gun Shooting
cnt=0
# 1 shot session allows 3 gun shots
while [ $cnt -le 2 ]; do
	echo "here: $cnt"
	cnt=$((cnt+1))

	python3 sound.py | while read line; do

	if [ "$line" = "detected!" ];
	then
		echo "$line"
		#./sendSigCapture : send sig_capture and receive coordinates. After receiving, print it at stdin, then exit program.

		line2=`./sendSigCapture sender sig_capture`  # via LoRa		
		echo "$line2" # for debugging

        #  increase variable cnt
		cnt=$((cnt+1))
		python3 giveCoordinates.py "$line2"  # via BT
	fi

	done
done


######### Phase #3 : Finish a Shot Session
./sendSigSessFin sender sig_sess_fin  # via LoRa

obexftp --nopath --noconn --uuid none --bluetooth A4:6C:F1:94:9E:24 --channel 5 -p /home/pi/ShotTracker/images/target.jpeg
