
from mpu6050 import mpu6050
from time import time
from datetime import datetime
from datetime import timedelta
from Adafruit_CharLCD import Adafruit_CharLCD
import csv
import cutie
import os, fnmatch
from glob import glob
from subprocess import check_output, CalledProcessError
from os.path import expanduser
import shutil

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

    endtime = time() + (360 * float(hours)) + (60 * float(minutes))

    print('Current time: {} Endtime: {}'.format(time(),endtime))
    print('Difference: {}'.format(endtime - time()))

    lcd.clear()
    lcd.message('ENTER TO START')
    raw_input('ENTER TO START')

    curTime = time()
    sensor = mpu6050(0x68)
    lcd = Adafruit_CharLCD()
    lcd.clear()

    finish = datetime.now() + timedelta(minutes = minutes) + timedelta(hours=hours)

    lcd.message('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))
    print('RECORDING...\nFINISH: {:02d}:{:02d}'.format(finish.hour, finish.minute))

    with open('{}.csv'.format(datetime.now()), 'w') as file:
        fieldnames = ['time', 'x', 'y', 'z']
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        while(endtime > curTime):
            accelerometer_data = sensor.get_accel_data()
            accelerometer_data['time'] = curTime
            writer.writerow(accelerometer_data)
            curTime = time()

    lcd.message('\nDONE')
    print('DONE')


################################################################################################

def transfer_data_usb():
    lcd = Adafruit_CharLCD()
    lcd.clear()

    #find usb and confirm hash
    usb = get_mount_points()

    while len(usb) == 0:
        options = ['Continue:', 'Back:']
        selected_option = cutie.select(options, selected_index=1)
        if selected_option == 'Back:':
            raise
        usb = get_mount_points()

    hashfile = find_file('hash', get_mount_points()[0][1])
    
    if hashfile is None:
        print('No hash file found on usb.')
        lcd.clear()
        lcd.message('INVALID USB')
        raise 

    #find all *.csv files and display select
    home = expanduser('~')
    csv_files = find_all_files('*.csv', home + '/mpu6050_raspi/mpu6050_raspi/')

    #transfer selected file to usb
    selected_csv = cutie.select(csv_files, selected_index=1)

    lcd.clear()
    lcd.message('COPYING FILE')
    shutil.copy(selected_csv, usb+'/'+selected_csv)
    time.sleep(1)

    #done
    lcd.clear()
    lcd.message('DONE')
    time.sleep(1)
    return

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    is_usb = lambda path: any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def find_all_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

################################################################################################

def main():
    """Main
    """
    
    while True:

        options = [
            'Record Data',
            'Transfer Data']    

        selected_option = cutie.select(options, selected_index=1)

        if selected_option == 0:
            record_data()
        elif selected_option == 1:
            transfer_data_usb()


if __name__ == '__main__':
    main()

