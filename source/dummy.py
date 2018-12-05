from Adafruit_CharLCD import Adafruit_CharLCD

from gpiozero import Button

from time import sleep

button_green = Button(2)
button_red = Button(3)
button_down = Button(4)
button_up = Button(17)

lcd = Adafruit_CharLCD()

def button_up_pressed():
	lcd.clear()
	lcd.message('Button UP pressed')
	sleep(1)

def button_down_pressed():
	lcd.clear()
	lcd.message('Button DOWN pressed')
	sleep(1)

def button_red_pressed():
	lcd.clear()
	lcd.message('Button RED pressed')
	sleep(1)

def button_green_pressed():
	lcd.clear()
	lcd.message('Button GREEN pressed')
	sleep(1)

if __name__ == "__main__":
	
	button_up.when_pressed = button_up_pressed
	button_down.when_pressed = button_down_pressed
	button_red.when_pressed = button_red_pressed
	button_green.when_pressed = button_green_pressed
	
	while True:
		lcd.clear()
		lcd.message('Waiting for Button')
