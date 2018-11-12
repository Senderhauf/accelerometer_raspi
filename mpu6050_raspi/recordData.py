
from mpu6050 import mpu6050
from time import time


sensor = mpu6050(0x68)

duration = ''

while('min' not in duration or 'hrs' not in duration):
    duration = raw_input('Enter duration (append min or hrs): ')
    if('min' not in duration or 'hrs' not in duration):
        print('Duration must be of type min or hrs')

endtime = None 

if 'min' in duration:
    endtime = time() + (60 * int(duration.split(" ")[0]))
else:
    endtime = time() + (360 * int(duration.split(" ")[0]))

raw_input('Press Enter to Start')

while(endtime > time()):
    accelerometer_data = sensor.get_accel_data()

print(accelerometer_data)