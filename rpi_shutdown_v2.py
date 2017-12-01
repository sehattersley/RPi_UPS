#!/usr/bin/python
# Author: sehattersley
# Version: v2 - Improved variable names
# Purpose: Shutdown the RPi when the power is lost and the RPi is running on battery backup. GPIO 3 (pin 5) is pulled
# to 0v when power is on by a transitor circuit, and is pulled to 3.3V by internal pull up resistor when power is off.
# This script should be run as cron job say every 20 mins.



# ---Imports---
import time # Used for the delay
from subprocess import call # Used for shutting down the Rpi using Python
import RPi.GPIO as GPIO # Used for reading the GPIO pin status



# ---Control Settings---
bDebug_Print = 1 # 0/1 will disable/enable debug print statements
nPin = 3 # GPIO pin


# ---Main Program---
GPIO.setwarnings(False)	# Disable warning such as channel already in use
GPIO.setmode(GPIO.BCM) # Reference pins by GPIO number. Use BOARD instead of BCM if you want to use pin numbers.
GPIO.setup(nPin, GPIO.IN)	#Set GPIO 3 (pin 5) as input
bPower_State = GPIO.input(nPin) # Read the status of the pin

if bDebug_Print == 1:
	if bPower_State == 1:
		print("GPIO3: " + str(bPower_State) + ", Power Off")
	if bPower_State == 0:
		print("GPIO3: " + str(bPower_State) + ", Power On")

if bPower_State == 1: # 1 means power is off. RPi will pull this high when floating.
	if bDebug_Print == 1:
		print("Power is off. Will check it again in 30 minutes")
	
	time.sleep(1800) # Keep running for 30 mins on battery power before checking if the power has resumed. Tune this to suit the battery capacity and frequency of cron job.
	bPower_State = GPIO.input(3) # Check pin again
	GPIO.cleanup()	# Release resorce
	
	if bPower_State == 1: # If the power is still off shutdown
		if bDebug_Print == 1:
			print("GPIO3: " + str(bPower_State) + ", Power is still off. RPi will now shutdown")
		call("sudo shutdown -h now", shell=True) # Shutdown the RPi
	else: # If power is back on
		if bDebug_Print == 1:
			print("GPIO3: " + str(bPower_State) + ", Power is back on")

if bDebug_Print == 1:
	print("Script Finished")
#End of script