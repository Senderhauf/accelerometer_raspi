#!/usr/bin/python

from record_data import record_data
from transfer_usb import transfer_usb
import system_functions
import myLCD
import cutie
import os
import schedule
from time import sleep, strftime

#press cancel button 5 times in a row to exit the program
cancel_count = 0

def select_option():
	options = [
		'RECORD DATA',
		'TRANSFER DATA', 
		'SYSTEM FUNCTIONS']
	selected_option = cutie.select(options, selected_index=0)

	if selected_option == -1:
		cancel_count += 1
	elif selected_option == 0:
		record_data()
		cancel_count = 0
	elif selected_option == 1:
		transfer_usb()
		cancel_count = 0
	elif selected_option == 2:
		options = [
			'DELETE FILE', 
			'SET CLOCK']
		selected_option = cutie.select(options, selected_index = 0)

		if selected_option == 0:
			system_functions.delete_file()
		elif selected_option == 1:
			system_functions.set_time()


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

	while True:
		select_option()
		cutie.getTime()

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

