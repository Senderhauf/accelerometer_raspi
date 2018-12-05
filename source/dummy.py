from Adafruit_CharLCD import Adafruit_CharLCD

from gpiozero import Button

button_green = Button(2)
button_red = Button(3)
button_down = Button(4)
button_up = Button(17)


def get_button_status():
    return {'up': button_up.is_pressed, 
            'down': button_down.is_pressed, 
            'green': button_green.is_pressed, 
            'red': button_red.is_pressed}

if __name__ == "__main__":
	
	lcd = Adafruit_CharLCD()
    lcd.clear()
	
	while True:
		button_status = get_button_status()
		if button_status['up']:
			lcd.message('Button status is UP')
		elif button_status['down']:
			lcd.message('Button status is DOWN')
		else:
			lcd.message('Button status is UKNOWN')
