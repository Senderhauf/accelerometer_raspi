from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from Adafruit_CharLCD import Adafruit_CharLCD
import csv
import cutie

def record_data():
    lcd = Adafruit_CharLCD()
    lcd.clear()

    duration = 0

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

    lcd.clear()
    lcd.message('ENTER TO START')
    raw_input('ENTER TO START')

    curTime = time()
    #sensor = mpu6050(0x68)
    lcd = Adafruit_CharLCD()
    lcd.clear()

    finish = datetime.now() + timedelta(minutes = minutes) + timedelta(hours=hours)

    lcd.message('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))
    print('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))


    # write function to check if /dev/ttyUSB0 is available (sensor is plugged in correctly)
    # excute following script: java -jar ~/BannerQM42TestApplication.jar -config 1000RPM-5Hz_1Device.JSON -logfile test.csv -port /dev/ttyUSB0

    with open('{}.csv'.format(datetime.now()), 'w') as file:
        fieldnames = ['time', 'x', 'y', 'z']
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        while(endtime > curTime):
            #accelerometer_data = {sensor.get_accel_data()}
            accelerometer_data = {}
            accelerometer_data['time'] = curTime
            writer.writerow(accelerometer_data)
            curTime = time()

    lcd.message('\nDONE')
    print('DONE')

