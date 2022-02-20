#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

################### Sound Detection ################### 
#GPIO SETUP
channel = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
cnt = 0


def callback(channel):
    if GPIO.input(channel):
        print("detected!")
        global cnt
        cnt = cnt + 1

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=700)
GPIO.add_event_callback(channel, callback)

while cnt < 1:
    time.sleep(1)
################### End of Sound Detection ################### 
