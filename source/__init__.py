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
	global cancel_count

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
	global cancel_count

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
		if cancel_count >= 3:
			myLCD.clear_all()
			options = ['EXIT', 'SHUTDOWN']
			selected_option = cutie.select(options, selected_index = 0)
			if selected_option == 0:
				myLCD.updateLCD(str2='EXITING PROGRAM', str3='GOODBYE')
				sleep(2)
				exit()
			elif selected_option == 1:
				myLCD.updateLCD(str2='EXITING PROGRAM', str3='GOODBYE')
				sleep(2)
				os.system('sudo shutdown now -h')

if __name__ == '__main__':
	main()
