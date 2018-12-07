
from record_data import record_data
from transfer_usb import transfer_usb
#from Adafruit_CharLCD import Adafruit_CharLCD

import myLCD
import cutie

def main():
    """Main
    """

	# Remove old shutdown file
	try:
		os.remove("/home/pi/accelerometer_raspi/source/shutdown")
	except (OSError):
		pass


	updateLCD(str2="WELCOME", str3="REXNORD EDGE DEVICE")
	clearLine(2)
	clearLine(3)

    while True:
        options = [
            'RECORD DATA',
            'TRANSFER DATA']    

        
        selected_option = cutie.select(options, selected_index=0)

        if selected_option == 0:
            record_data()
        elif selected_option == 1:
            transfer_usb()

        # update lcd every 100 ms
        updateLCD()


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

