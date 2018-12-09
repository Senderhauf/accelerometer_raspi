from time import sleep
from os.path import expanduser
import myLCD, cutie
import subprocess, os, fnmatch


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
	selected_index = cutie.select(csv_files_lcd, selected_index=0)
	if selected_index == -1:
		return
	selected_csv = csv_files[selected_index]

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

def _set_time_helper(time_tuple):
	cmd = 'sudo date --set=\'{}-{}-{}'.format(time_tuple[0], time_tuple[1], time_tuple[2])
    subprocess.check_output(cmd.split())

    cmd = 'sudo date --set=\'{}:{}\''.format(time_tuple[3],time_tuple[4])
    subprocess.check_output(cmd.split())

def set_time():
	
	myLCD.clear_all()

	myLCD.updateLCD(str2='SET TIME')
	year = cutie.get_number_arrows('YEAR', 1, 2050, 2018)
	if year == -1:
		return

	myLCD.updateLCD(str2='SET TIME')
	month = cutie.get_number_arrows('MONTH', 1, 13, 1)
	if year == -1:
		return 

	invalidDay = True
	day = 0
	while invalidDay:
		myLCD.updateLCD(str2='SET TIME')
		day = cutie.get_number_arrows('DAY', 1, 32, 1)
		
		if day == -1:
			return 

		if day == 31 and (month in [2,4,6,9,11]):
			invalidDay = True
			myLCD.updateLCD(str2='INVALID DAY')

		elif day == 30 and (month in [2]):
			myLCD.updateLCD(str2='INVALID DAY')
			invalidDay = True
		else:
			invalidDay = False
	
	myLCD.updateLCD(str2='SET TIME')
	hour = cutie.get_number_arrows('HOUR', 1, 13, 1)
	if hour == -1:
		return

	myLCD.updateLCD(str2='SET TIME')
	minute = cutie.get_number_arrows('MINUTE', 1, 60, 1)	
	if hour == -1:
		return

	time_tuple = ( year, 
	                month, 
	                day, 
	                hour, 
	                minute, 
	            )
	
	_set_time_helper(time_tuple)

	myLCD.clear_all()
