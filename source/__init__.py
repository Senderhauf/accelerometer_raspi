
from record_data import record_data
from transfer_usb import transfer_usb
from Adafruit_CharLCD import Adafruit_CharLCD

import cutie

def main():
    """Main
    """
    
    while True:

        options = [
            'RECORD DATA',
            'TRANSFER DATA']    

        try:
            selected_option = cutie.select(options, selected_index=0)

            if selected_option == 0:
                record_data()
            elif selected_option == 1:
                transfer_usb()
        except:
            continue

        finally:
            lcd = Adafruit_CharLCD()
            lcd.message('Error. Restart Module.')
            lcd.clear()

if __name__ == '__main__':
    main()

