#!/usr/bin/python

from record_data import record_data
from transfer_usb import transfer_usb
import myLCD
import cutie
import os
import schedule
from time import sleep, strftime

def getTime():
	"Gets the current time and date and sets the LCDs 1st row"
	time=strftime("%A %Y-%m-%d %H:%M:%S")
	myLCD.printLine(0, time)


def select_option():
	options = [
		'RECORD DATA',
		'TRANSFER DATA']
	selected_option = cutie.select(options, selected_index=0)

	if selected_option == 0:
		record_data()
	elif selected_option == 1:
		transfer_usb()

def main():
# Remove old shutdown file
	try:
		os.remove("/home/pi/accelerometer_raspi/source/shutdown")
	except (OSError):
		pass
	
	myLCD.updateLCD(str2="WELCOME", str3="REXNORD EDGE DEVICE")
	sleep(2)

	myLCD.clearLine(2)
	myLCD.clearLine(3)

	schedule.every(.1).seconds.do(getTime)

	while True:
		selected_option()

		# update lcd every 100 ms
		myLCD.updateLCD()


if __name__ == '__main__':
	main()


'''
### MAIN FUNCTION
while True:
	schedule.run_pending()
	time.sleep(0.01)
	#Check if shutting down
	try:
		if os.path.isfile("/home/pi/RPi-LCD/shutdown"):
			print "Shutting down"
			shutdown_message()
	except (OSError):
		pass
	#Update LCD every 100 ms
	updateLCD()	
'''

