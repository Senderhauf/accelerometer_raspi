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
