
from mpu6050 import mpu6050
from time import time
from datetime import datetime
import csv
import cutie


def record_data():
    

    if cutie.prompt_min_or_hour('Enter duration type:'):



    duration = ''

    while('min' not in duration and 'hrs' not in duration):
        duration = input('Enter duration (append min or hrs): ')
        if('min' not in duration and 'hrs' not in duration):
            print('Duration must be of type min or hrs')

    endtime = None

    if 'min' in duration:
        endtime = time() + (60 * float(duration.split(" ")[0]))
    else:
        endtime = time() + (360 * float(duration.split(" ")[0]))

    input('Press Enter to Start')

    curTime = time();

    with open('{}.csv'.format(datetime.now()), 'w') as file:
        fieldnames = ['time', 'x', 'y', 'z']
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        while(endtime > curTime):
            accelerometer_data = sensor.get_accel_data()
            accelerometer_data['time'] = curTime
            writer.writerow(accelerometer_data)
            curTime = time()

def transfer_data_usb():


def interface_pc():


def main():
    """Main
    """

    options = [
        'Options:',
        'Record Data',
        'Transfer Data', 
        'Connect to PC']

    captions = [0]

    selected_option = cutie.select(options, caption_indices=captions, selected_index=1)

    if selected_option == 1:
        record_data()
    elif selected_option == 2:
        transfer_data_usb()
    else:
        interface_pc()



if __name__ == '__main__':
    main()

