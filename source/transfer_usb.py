
from Adafruit_CharLCD import Adafruit_CharLCD
import csv
import cutie
import os, fnmatch
from glob import glob
import subprocess
from os.path import expanduser
import shutil
from time import sleep
import myLCD

def transfer_usb():

	myLCD.clear_all()

	#find usb and confirm hash
	usb = get_usb_devices()

	while len(usb) == 0:
		myLCD.printLine(1, 'NO USB CONNECTED')
		print('NO USB CONNECTED')
		sleep(1)
		options = ['CONNECT USB', 'BACK']
		selected_option = cutie.select(options, selected_index=0)
		if selected_option == 1:
			return	# back to main menu
		usb = get_usb_devices()


	# mount usb device if necessary
	usb_mount_pt = get_mount_points()

	mount_types = ['ext3', 'ext2', 'ext4', 'vfat']

	if len(usb_mount_pt) == 0:
		# mount should iterate through all file system types in /proc/filesystems but fails itermittently
	    for mount_type in mount_types:
		    bash_mount_cmd = 'sudo mount -t {} /dev/{} /media/usb/'.format( mount_type, usb.keys()[0])
		    print(bash_mount_cmd)
		    subprocess.Popen(bash_mount_cmd.split())

	hashfile = find_file('hash.key', '/media/usb/')

	if hashfile is None:
		print('INVALID USB')
		myLCD.printLine(1, 'INVALID USB')
		sleep(1)
		return # back to main menu

	# find all *.csv files and display select
	home = expanduser('~')
	csv_files = find_all_files('*.csv', home)

	csv_files_lcd = [] 
	for file in csv_files:
		strs = file.split('_')
		tmp = strs[1]+strs[2]
		tmp = tmp[:tmp.rfind(':')]
		csv_files_lcd.append(tmp)

	#transfer selected file to usb
	myLCD.clear_all()
	selected_csv = csv_files[cutie.select(csv_files_lcd, selected_index=0)]
	print('SELECTED CSV: '+ selected_csv)

	myLCD.updateLCD(str2='COPYING FILE', str3='DO NOT UNPLUG USB')
	#shutil.copy(selected_csv, '/media/usb'+selected_csv)

	# hacky workaround using bash executed in python 
	cmd = 'sudo chmod 777 /media/usb'
	subprocess.check_output(cmd.split())

	selected_csv_file = selected_csv.split('/')[-1]
	selected_csv_file = selected_csv_file.replace(' ', '')

	cmd = 'touch /media/usb/{}'.format(selected_csv_file)
	#subprocess.check_output(cmd.split())

	cmd = 'sudo cp {} /media/usb/{}'.format(selected_csv, selected_csv_file)
	cmd = cmd.split()
	cmd = cmd[:2] + [cmd[2]+' '+cmd[3]] + cmd[4:]
	subprocess.check_output(cmd)

	sleep(1)

	#done
	myLCD.updateLCD(str2='TRANSFER COMPLETE')
	print('DONE')
	sleep(1)
	return

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)


def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = subprocess.check_output(['mount']).splitlines()
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
