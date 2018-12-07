#!/usr/bin/python


##Time
from datetime import datetime, timedelta
from time import gmtime, strftime, sleep

##Data Acqusition
from xml.dom import minidom
import urllib2
import json
import feedparser

##Scheduling
import schedule
import time

## Raspberry libraries
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/accelerometer_raspi/source/RPLCD')
from RPLCD.gpio import CharLCD

## Shutdown management
import os.path

##define staic values

## LCD SETUP
### Pin number has to be change to the pin numbers you are using on your Raspberry Pi.
### The LCD is a 40x4 display. The library RPLCD can only handle 40x2 so the LCD has to be set up as two 40x2 displays.
### using two enable signals. The handling of this is done under LCD handler.
### The number are the pin numbers of the Raspberry Pi, not the GPIO numbers.
### If using a older Raspberry Pi with only 26 pins make sure you have the correct pin pinnumbers.

GPIO_PIN_RS = 37
GPIO_PIN_RW = None ## Raspberry Pi cannot handle if the display writes data. Could damage RPi. This pin on the LCD was connected to gound.
GPIO_PIN_E_TOP = 35
GPIO_PIN_E_BOTTOM = 40
GPIO_PIN_D4 = 33
GPIO_PIN_D5 = 31
GPIO_PIN_D6 = 29
GPIO_PIN_D7 = 23
LCD_COLUMNS = 40
LCD_ROWS = 2
LCD_DOT_SIZE = 8

LCD_BRIGHTNESS = 0 # to be used with PWM for control of the LCD brightness.

### Initialize the LCD
lcd_top = CharLCD(pin_rs=GPIO_PIN_RS, pin_rw=GPIO_PIN_RW,  pin_e=GPIO_PIN_E_TOP, pins_data=[GPIO_PIN_D4, GPIO_PIN_D5, GPIO_PIN_D6, GPIO_PIN_D7], numbering_mode=GPIO.BOARD, cols=LCD_COLUMNS, rows=LCD_ROWS, dotsize=LCD_DOT_SIZE)
lcd_bottom = CharLCD(pin_rs=GPIO_PIN_RS, pin_rw=GPIO_PIN_RW, pin_e=GPIO_PIN_E_BOTTOM, pins_data=[GPIO_PIN_D4, GPIO_PIN_D5, GPIO_PIN_D6, GPIO_PIN_D7], numbering_mode=GPIO.BOARD, cols=LCD_COLUMNS, rows=LCD_ROWS, dotsize=LCD_DOT_SIZE)

var = 1
i = 0


### Functions for getting time
def getTime():
	"Gets the current time and date and returns as a string"
	time=strftime("%A %Y-%m-%d %H:%M:%S")
	return time


def getPercent(now,then):
	percents = []
	nbr = len(now)	
	for i in range(0, nbr):
		#print float(now[i])
		#print float(then[i])
		percent = 100*(float(now[i]) - float(then[i]))/float(then[i])
		#print percent
		percents.append(str("%.2f" % percent))

	return percents
		 
### LCD Functions
def printLine( lineNr, str):
	#Add spaces for automatic clearing of LCD
	str+="                                            "
	"Prints one line on LCD, lineNR, 0-3 is LCD Row and str is string to be printed, max 40 char (will be cropped if longer)"
	str=str[:40] #Crop string to first 40 char
	# If lineNr 0 or 1, top LCD
	if lineNr==0 or lineNr==1:
		lcd_top.cursor_pos=(lineNr,0)
		lcd_top.write_string(str)
	# If lineNr 2 or 3, bottom LCD
	elif lineNr==2 or lineNr==3:
		lineNr-=2 #Still called as row 0,1 to lcd...
		lcd_bottom.cursor_pos=(lineNr,0)
		lcd_bottom.write_string(str)
	return

def clearLine(lineNr):
	printLine(lineNr, "                                            ")
	return

def firstString():
	"Creates first string for LCD"
	str = getTime()
	return str

def secondString():
	"Creates second string for LCD"
	str = ""
	return str

def thirdString():
	"Creates third string for LCD"
	'''
	my_news = "          "+curNews[news_count]
	str = "News: "+my_news[scrollCount:scrollCount+34]
	global scrollCount
	scrollCount +=1
	'''
	str = ""
	return str

def fourthString():
	"Creates fourth string for LCD"
	str = ""
	return str

def updateLCD(str1=getTime(), str2="", str3="", str4=""):
	printLine(0,firstString())
        printLine(1,secondString())
	printLine(2,thirdString())
        printLine(3,fourthString())
	#print "LCD update"	

## Shutdown management
def shutdown_message():
	# Print shutdown message
	printLine(0,40*'-')
        printLine(1,13*' '+"Shutting down")
	printLine(2,5*' '+"Re-plug power cable to restart")
        printLine(3,40*'-')
	# Terminate LCD program
	quit()
	

	
