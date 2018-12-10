from time import time
from time import sleep
import datetime 
from Adafruit_CharLCD import Adafruit_CharLCD
import csv
import cutie
import os
import signal
import subprocess
import myLCD

def record_data():
    # lcd = Adafruit_CharLCD()
    # lcd.clear()

    hours = 0
    minutes = 0

    myLCD.clear_all()
    myLCD.printLine(1, 'ENTER DURATION:')
    hours = cutie.get_number_arrows('HOURS', 1, 13, 0)
    if hours == -1:
    	return
    minutes = cutie.get_number_arrows('MIN', 1, 60, 0)
    if minutes == -1:
    	return

    if minutes+hours == 0:
    	#lcd.clear()
    	#lcd.message('NO TIME ENTERED')
        myLCD.updateLCD(str2 = 'NO TIME ENTERED')
    	print('NO TIME ENTERED')
    	sleep(1)
    	return

    endTime = time() + (3600 * float(hours)) + (60 * float(minutes))

    # check if sensor is attached via /dev/ttyUSB0
    sensor_connected = os.path.exists('/dev/ttyUSB0')
    while not sensor_connected:
        #lcd.clear()
        #lcd.message('NO SENSOR FOUND')
        myLCD.updateLCD(str2 = 'NO SENSOR FOUND')
        print('NO SENSOR FOUND')
        sleep(1)
        options = ['RETRY SENSOR PAIRING']
        selected_option = cutie.select(options, selected_index=0)
        if selected_option == -1:
            return # back to main menu
        sensor_connected = os.path.exists('/dev/ttyUSB0')

    myLCD.updateLCD(str2='ENTER TO START')
    button_pressed = None
    while button_pressed != 'green' or button_pressed != 'red':
        myLCD.getTime()
        button_pressed = myLCD.wait_for_button()

    if button_pressed == 'red':
        myLCD.updateLCD(str2='CANCELING...')
        sleep(1)
        return

    # calculate the finish time after the user confirms the start 
    curTime = time()
    finish = datetime.datetime.fromtimestamp(endTime)

    myLCD.printLine(2, 'RECORDING...')
    myLCD.updateLCD(str4='FINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))
    print('FINISH: {:02d}:{:02d}\nRECORDING...'.format(finish.hour, finish.minute))
 
    # excute following script: java -jar ~/BannerQM42TestApplication.jar -config 1000RPM-5Hz_1Device.JSON -logfile test.csv -port /dev/ttyUSB0
    os.chdir('/home/pi')
    cmd = 'java -jar BannerQM42TestApplication.jar -config 1000RPM-5Hz_1Device.JSON -logfile {}.csv -port /dev/ttyUSB0'
    cmd = cmd.format(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    #subprocess.check_output(cmd.split())

    # see StackO: https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    pro = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, preexec_fn=os.setsid)

    while True:
        myLCD.getTime()
        button_pressed = myLCD.wait_for_button()
        if(time() >= endTime):
            break

    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

    os.chdir('/home/pi/accelerometer_raspi/source')

    #lcd.message('\nDONE')
    myLCD.updateLCD(str2='DONE')
    print('DONE')

