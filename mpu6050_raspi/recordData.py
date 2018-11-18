
from mpu6050 import mpu6050
from time import time
from datetime import datetime
import csv
import cutie


def record_data():

    is_min_type = cutie.prompt_min_or_hour('Enter duration type: ') == 'min'

    duration = 0

    if is_min_type:
        duration = cutie.get_number_arrows('Enter duration ', 5, 60, 0)

        # endtime = time() + (60 * float(duration))
        endtime = time() + (float(duration))

    else:
        duration = cutie.get_number_arrows('Enter duration ', 5, 60, 0)

        endtime = time() + (360 * float(duration))

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
    return

def interface_pc():
    return

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

