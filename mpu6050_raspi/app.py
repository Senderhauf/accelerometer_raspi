
from .record_data import record_data
from .transfer_usb import transfer_usb

def main():
    """Main
    """
    
    while True:

        options = [
            'RECORD DATA',
            'TRANSFER DATA']    

        selected_option = cutie.select(options, selected_index=0)

        if selected_option == 0:
            record_data()
        elif selected_option == 1:
            transfer_usb()


if __name__ == '__main__':
    main()

