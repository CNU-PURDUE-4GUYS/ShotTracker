#!/bin/bash

cnt=0
######### Phase #2 : Gun Shooting
#while [ $cnt -eq 3 ]; do

while [ $cnt -le 2 ]; do
	echo "here: $cnt"
	cnt=$((cnt+1))

	python3 sound.py | while read line; do
	# echo "$line"

	if [ "$line" = "detected!" ];
	then
		echo "$line"
		#./sendSigCapture : send sig_capture and receive coordinates. After receiving, print it at stdin, then exit program.

		line2=`./sendSigCapture sender sig_capture`  # via LoRa
		
		#./sendSigCapture sender sig_capture | while read line; do
		echo "$line2"

		cnt=$((cnt+1))
	#	echo "count: $cnt"
		python3 giveCoordinates.py "$line2"  # via BT
		
	#	if [ $cnt -eq 3 ];
	#	then

	#		break
	#	fi
	#	break
	fi

done
done
######### Phase #3 : Finish a Shot Session

#./sendSigSessFin sender sig_sess_fin  # via LoRa

obexftp --nopath --noconn --uuid none --bluetooth A4:6C:F1:94:9E:24 --channel 5 -p /home/pi/ShotTracker/images/target.jpeg
#		break
#	fi
#done
