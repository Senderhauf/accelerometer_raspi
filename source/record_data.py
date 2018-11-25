from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from Adafruit_CharLCD import Adafruit_CharLCD
import csv
import cutie
import os.path
import sys
import subprocess

def record_data():
    lcd = Adafruit_CharLCD()
    lcd.clear()

    hours = 0
    minutes = 0

    hours = cutie.get_number_arrows('HOURS', 1, 13, 0)
    if hours == -1:
    	return
    minutes = cutie.get_number_arrows('MIN', 1, 60, 0)
    if minutes == -1:
    	return

    if minutes+hours == 0:
    	lcd.clear()
    	lcd.message('NO TIME ENTERED')
    	print('NO TIME ENTERED')
    	sleep(1)
    	return

    endtime = time() + (3600 * float(hours)) + (60 * float(minutes))

    # check if sensor is attached via /dev/ttyUSB0
    sensor_connected = os.path.exists('/dev/ttyUSB0')
    while not sensor_connected:
        lcd.clear()
        lcd.message('NO SENSOR FOUND')
        print('NO SENSOR FOUND')
        sleep(1)
        options = ['CONNECT SENSOR', 'BACK']
        selected_option = cutie.select(options, selected_index=0)
        if selected_option == 1:
            return # back to main menu
        sensor_connected = os.path.exists('/dev/ttyUSB0')

    lcd.clear()
    lcd.message('ENTER TO START')
    raw_input('ENTER TO START')

    curTime = time()
    finish = datetime.now() + timedelta(minutes = minutes) + timedelta(hours=hours)

    lcd.clear()
    lcd.message('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))
    print('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))
 
    # excute following script: java -jar ~/BannerQM42TestApplication.jar -config 1000RPM-5Hz_1Device.JSON -logfile test.csv -port /dev/ttyUSB0
    sys.path.append('/home/pi')
    cmd = 'java -jar BannerQM42TestApplication.jar -config 1000RPM-5Hz_1Device.JSON -logfile {}{}.csv -port /dev/ttyUSB0'.format(os.path.expanduser('~')+'/accelerometer_raspi/data/', datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    subprocess.check_output(cmd.split())
    sys.path.append('/home/pi/accelerometer_raspi/source')

    lcd.message('\nDONE')
    print('DONE')

