from time import sleep
from os.path import expanduser
import myLCD, cutie
import subprocess, os, fnmatch
import sys
import datetime
import ctypes
import ctypes.util
import time

def delete_file():
	myLCD.clear_all()

	# find all *.csv files and display select
	home = expanduser('~')
	csv_files = find_all_files('*.csv', home)

	if len(csv_files) == 0:
		myLCD.updateLCD(str2='NO FILES FOUND')

	csv_files_lcd = [] 
	count = 1
	for file in csv_files:
		strs = file.split('_')
		tmp = str(count)+'. '+strs[1]+' '+strs[2]
		#tmp = tmp[:tmp.rfind(':')]
		csv_files_lcd.append(tmp)
		count += 1

	#transfer selected file to usb
	myLCD.clear_all()
	selected_csv = csv_files[cutie.select(csv_files_lcd, selected_index=0)]
	print('SELECTED CSV: '+ selected_csv)

	myLCD.updateLCD(str2='SELECTED CSV: ', str3=selected_csv.split('Device')[1][2:], str4='DELETING FILE')

	os.remove(selected_csv)
	sleep(1)

	myLCD.updateLCD(str4='FILE DELETED')
	sleep(1)

	return

def find_all_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def _linux_set_time(time_tuple):

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime.datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

def set_time():
	
	myLCD.clear_all()

	myLCD.updateLCD(str2='SET TIME')
	year = cutie.get_number_arrows('YEAR', 1, 2050, 2018)

	myLCD.updateLCD(str2='SET TIME')
	month = cutie.get_number_arrows('MONTH', 1, 13, 1)
	
	invalidDay = True
	day = 0
	while invalidDay:
		myLCD.updateLCD(str2='SET TIME')
		day = cutie.get_number_arrows('DAY', 1, 32, 1)
		
		if day == 31 and (month in [2,4,6,9,11])
			invalidDay = True
			myLCD.updateLCD(str2='INVALID DAY')

		elif day == 30 and (month in [2])
			myLCD.updateLCD(str2='INVALID DAY')
			invalidDay = True
		else:
			invalidDay = False
	
	myLCD.updateLCD(str2='SET TIME')
	hour = cutie.get_number_arrows('HOUR', 1, 13, 1)
	
	myLCD.updateLCD(str2='SET TIME')
	minute = cutie.get_number_arrows('MINUTE', 1, 60, 1)	

	time_tuple = ( year, 
	                month, 
	                day, 
	                hour, 
	                minute, 
	                0, 
	                0, # Millisecond
	            )

	_linux_set_time(time_tuple)
