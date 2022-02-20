#!/bin/bash

while true; do

######### Phase #1 : Target Setting
targetNumber=python3 receiveTargetNumber.py # via BT

ACK=./sendTargetNumber sender $targetNumber # via LoRa

# if ACK received, then give ACK to Android
#./sendTargetNumber | while read line; do
if [ "$ACK" = "ACK" ]
then 
	python3 giveACK.py  # via BT


######### Phase #2 : Gun Shooting
while true; do
	python3 shooting.py | while read line; do
	if [ "$line" = "detected!" ]
	then
		#./sendSigCapture : send sig_capture and receive coordinates. After receiving, print it at stdin, then exit program.
		./sendSigCapture | while read line; do # via LoRa
		if [ "$line" != "" ]	#  when $line gets the coordinates, then give it to Android.
		then
			line | python3 giveCoordinates.py  # via BT
			break


######### Phase #3 : Finish a Shot Session
	elif [ "$line" = "finish" ]
	then
		./sendSigSessFin
		./receiveImage
		break
	fi
done

