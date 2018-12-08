
from __future__ import print_function
import sys

import getpass
#from typing import List, Optional

from colorama import init
import readchar

import Adafruit_CharLCD
import myLCD
from myLCD import getTime

from gpiozero import Button

from signal import pause
from time import sleep, strftime

button_green = Button(3)
button_red = Button(2)
button_down = Button(4)
button_up = Button(17)


init()

def wait_for_button():
    button_up_pressed = False
    button_down_pressed = False
    button_red_pressed = False
    button_green_pressed = False

    button_up_pressed = button_up.wait_for_press(.01)
    button_down_pressed = button_down.wait_for_press(.01)
    button_red_pressed = button_red.wait_for_press(.01)
    button_green_pressed = button_green.wait_for_press(.01)

    sleep(.15)
    
    if button_up_pressed:
        return 'up'
    elif button_down_pressed:
        return 'down'
    elif button_green_pressed:
        return 'green'
    elif button_red_pressed:
        return 'red'
    else:
        return None

def get_number(
        prompt,                        # type: str
        min_value = None,  # type: Optional[float]
        max_value = None,  # type: Optional[float]
        allow_float = True): # type: bool
    #type: (...) -> float
    """Get a number from user input.
    If an invalid number is entered the user will be prompted again.

    Args:
        prompt (str): The prompt asking the user to input.
        min_value (float, optional): The [inclusive] minimum value.
        max_value (float, optional): The [inclusive] maximum value.
        allow_float (bool, optional): Allow floats or force integers.

    Returns:
        float: The number input by the user.
    """
    return_value = None
    while return_value is None:
        input_value = input(prompt + ' ')
        try:
            return_value = float(input_value)
        except ValueError:
            print('Not a valid number.\033[K\033[1A\r\033[K', end='')
        if not allow_float and return_value is not None:
            if return_value != int(return_value):
                print('Has to be an integer.\033[K\033[1A\r\033[K', end='')
                return_value = None
        if min_value is not None and return_value is not None:
            if return_value < min_value:
                print('Has to be at least {}.\033[K\033[1A\r\033[K'.format(min_value),
                      end='')
                return_value = None
        if max_value is not None and return_value is not None:
            if return_value > max_value:
                print('Has to be at most {}.\033[1A\r\033[K'.format(max_value), end='')
                return_value = None
        if return_value is not None:
            break
    print('\033[K', end='')
    if allow_float:
        return return_value
    return int(return_value)


def secure_input(prompt):   #type: str
    #type: (...) -> str
    """Get secure input without showing it in the command line.

    Args:
        prompt (str): The prompt asking the user to input.

    Returns:
        str: The secure input.
    """
    return getpass.getpass(prompt + ' ')


def select(
        options ,             # type: List[str]
        caption_indices = None,    # type: Optional[List[int]]
        deselected_prefix = '\033[1m[ ]\033[0m ',  # type: str
        selected_prefix = '\033[1m[\033[32;1mx\033[0;1m]\033[0m ', # type: str
        caption_prefix = '',   # type: str
        selected_index = 0):    # type: int 
    #type: (...) -> int
    """Select an option from a list.

    Args:
        options (List[str]): The options to select from.
        caption_indices (List[int], optional): Non-selectable indices.
        deselected_prefix (str, optional): Prefix for deselected option ([ ]).
        selected_prefix (str, optional): Prefix for selected option ([x]).
        caption_prefix (str, optional): Prefix for captions ().
        selected_index (int, optional): The index to be selected at first.

    Returns:
        int: The index that has been selected.
    """

    #lcd = Adafruit_CharLCD()
    #lcd.clear()
    lcd_deselected_prefix = '[ ]'
    lcd_selected_prefix = '[x]'
    myLCD.updateLCD()
    print('\n' * (len(options) - 1))
    if caption_indices is None:
        caption_indices = []


    '''
        Get selected index 
        if there are at least two options above the selected index 
            show only two options above and the one selected
        else 
            print items as before
    '''

    while True:
        getTime()
        print('\033[{}A'.format(len(options) + 1))

        for i, option in enumerate(options):

            if i not in caption_indices:
                print('\033[K{}{}'.format(
                    selected_prefix if i == selected_index else
                    deselected_prefix, option))
                # if the selected index is at least 
                if (selected_index > 2 and i < selected_index and i > selected_index-3):
                    print('i: {}, selected_index: {}'.format(i, selected_index))
                    if (selected_index-i == 2):
                        lineNum = 0
                    elif (selected_index-i == 1):
                        lineNum = 1
                    else:
                        lineNum = 2
                    myLCD.printLine(lineNum, '{}{}\n'.format(
                        lcd_selected_prefix if i == selected_index else
                        lcd_deselected_prefix, option))
                elif (i < 3):
                    myLCD.printLine(i+1, '{}{}\n'.format(
                        lcd_selected_prefix if i == selected_index else
                        lcd_deselected_prefix, option))
            elif i in caption_indices:
                #print('\033[K{}{}'.format(caption_prefix, options[i]))
                myLCD.printLine(i+1, '{}{}'.format(caption_prefix, options[i]))

        #keypress = readchar.readkey()
        #keypress = None

        button_pressed = None

        while button_pressed is None:
            getTime()
            button_pressed = wait_for_button()

        #if keypress == readchar.key.UP or button_up_pressed:
        if button_pressed == 'up':
            new_index = selected_index
            while new_index > 0:
                new_index -= 1
                if new_index not in caption_indices:
                    selected_index = new_index
                    break
        #elif keypress == readchar.key.DOWN or button_down_pressed:
        elif button_pressed == 'down':
            new_index = selected_index
            while new_index < len(options) - 1:
                new_index += 1
                if new_index not in caption_indices:
                    selected_index = new_index
                    break
        else:
            break
    return selected_index


def select_multiple(
        options,     # type: List[str]
        caption_indices = None,    # type: Optional[List[int]]
        deselected_unticked_prefix = '\033[1m( )\033[0m ', # type: str
        deselected_ticked_prefix = '\033[1m(\033[32mx\033[0;1m)\033[0m ',  # type: str 
        selected_unticked_prefix = '\033[32;1m{ }\033[0m ',    # type: str
        selected_ticked_prefix = '\033[32;1m{x}\033[0m ',  # type: str 
        caption_prefix = '',   # type: str
        ticked_indices = None, # type: Optional[List[int]]
        cursor_index = 0,  # type: int
        minimal_count = 0, # type: int
        maximal_count = None,    # type: Optional[int] 
        hide_confirm = False, # type: bool
        deselected_confirm_label = '\033[1m(( confirm ))\033[0m',  # type: str
        selected_confirm_label = '\033[1;32m{{ confirm }}\033[0m', # type: str
    ):
    #type: (...) -> List[int] 
    """Select multiple options from a list.

    Args:
        options (List[str]): The options to select from.
        caption_indices (List[int], optional): Non-selectable indices.
        deselected_unticked_prefix (str, optional): Prefix for lines that are
            not selected and not ticked (( )).
        deselected_ticked_prefix (str, optional): Prefix for lines that are
            not selected but ticked ((x)).
        selected_unticked_prefix (str, optional): Prefix for lines that are
            selected but not ticked ({ }).
        selected_ticked_prefix (str, optional): Prefix for lines that are
            selected and ticked ({x}).
        caption_prefix (str, optional): Prefix for captions ().
        ticked_indices (List[int], optional): Indices that are
            ticked initially.
        cursor_index (int, optional): The index the cursor starts at.
        minimal_count (int, optional): The minimal amount of lines
            that have to be ticked.
        maximal_count (int, optional): The maximal amount of lines
            that have to be ticked.
        hide_confirm (bool, optional): Hide the confirm button.
            This causes <ENTER> to confirm the entire selection and not just
            tick the line.
        deselected_confirm_label (str, optional): The confirm label
            if not selected ((( confirm ))).
        selected_confirm_label (str, optional): The confirm label
            if selected ({{ confirm }}).

    Returns:
        List[int]: The indices that have been selected
    """
    print('\n' * (len(options) - 1))
    if caption_indices is None:
        caption_indices = []
    if ticked_indices is None:
        ticked_indices = []
    tick_keys = [' ']
    max_index = len(options) - (1 if hide_confirm else 0)
    if not hide_confirm:
        tick_keys.append(readchar.key.ENTER)
    error_message = ''
    while True:
        print('\033[{}A'.format(max_index + 2))
        for i, option in enumerate(options):
            prefix = ''
            if i in caption_indices:
                prefix = caption_prefix
            elif i == cursor_index:
                if i in ticked_indices:
                    prefix = selected_ticked_prefix
                else:
                    prefix = selected_unticked_prefix
            else:
                if i in ticked_indices:
                    prefix = deselected_ticked_prefix
                else:
                    prefix = deselected_unticked_prefix
            print('\033[K{}{}'.format(prefix, option))
        if not hide_confirm:
            if cursor_index == max_index:
                print('{} {}\033[K'.format(selected_confirm_label, error_message))
            else:
                print('{} {}\033[K'.format(deselected_confirm_label, error_message))
        error_message = ''
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            new_index = cursor_index
            while new_index > 0:
                new_index -= 1
                if new_index not in caption_indices:
                    cursor_index = new_index
                    break
        elif keypress == readchar.key.DOWN:
            new_index = cursor_index
            while new_index + 1 <= max_index:
                new_index += 1
                if new_index not in caption_indices:
                    cursor_index = new_index
                    break
        elif keypress in tick_keys:
            if cursor_index == max_index and not hide_confirm:
                if minimal_count > len(ticked_indices):
                    error_message = \
                        'Must select at least {} options'.format(minimal_count)
                elif maximal_count is not None and\
                        maximal_count < len(ticked_indices):
                    error_message = \
                        'Must select at most {} options'.format(maximal_count)
                else:
                    break
            elif cursor_index in ticked_indices:
                if len(ticked_indices) - 1 >= minimal_count:
                    ticked_indices.remove(cursor_index)
            elif maximal_count is not None:
                if len(ticked_indices) + 1 <= maximal_count:
                    ticked_indices.append(cursor_index)
            else:
                ticked_indices.append(cursor_index)
        else:
            if minimal_count > len(ticked_indices):
                error_message = \
                    'Must select at least {} options'.format(minimal_count)
            elif maximal_count is not None and\
                    maximal_count < len(ticked_indices):
                error_message = \
                    'Must select at most {} options'.format(maximal_count)
            else:
                break
    if not hide_confirm:
        print('\033[1A\033[K', end='')
        sys.stdout.flush()
    return ticked_indices


def prompt_yes_or_no(
        question,  # type: str
        yes_text = 'Yes',  # type: str 
        no_text = 'No',    # type: str
        has_to_match_case = False,    # type: bool 
        enter_empty_confirms = True,  # type: bool
        default_is_yes = False,   # type: bool
        deselected_prefix = '  ',  # type: str
        selected_prefix = '\033[31m>\033[0m ', # type: str 
        abort_value = None, # type: Optional[bool]
        char_prompt = True):    # type: bool
    #type: (...) ->  Optional[bool]
    """Prompt the user to input yes or no.

    Args:
        question (str): The prompt asking the user to input.
        yes_text (str, optional): The text corresponding to 'yes'.
        no_text (str, optional): The text corresponding to 'no'.
        has_to_match_case (bool, optional): Does the case have to match.
        enter_empty_confirms (bool, optional): Does enter on empty string work.
        default_is_yes (bool, optional): Is yes selected by default (no).
        deselected_prefix (str, optional): Prefix if something is deselected.
        selected_prefix (str, optional): Prefix if something is selected (> )
        abort_value (bool, optional): The value to return on interrupt.
        char_prompt (bool, optional): Add a [Y/N] to the prompt.

    Returns:
        Optional[bool]: The bool what has been selected.
    """
    is_yes = default_is_yes
    is_selected = enter_empty_confirms
    current_message = ''
    yn_prompt = ' ({}/{}) '.format(yes_text[0], no_text[0]) if char_prompt else ': '
    abort = False
    print()
    while True:
        yes = is_yes and is_selected
        no = not is_yes and is_selected
        print('\033[K'
              '{}{}'.format(selected_prefix if yes else deselected_prefix, yes_text))
        print('\033[K'
              '{}{}'.format(selected_prefix if no else deselected_prefix, no_text))
        print('\033[3A\r\033[K'
              '{}{}{}'.format(question, yn_prompt, current_message), end='')
        sys.stdout.flush()

        keypress = readchar.readkey()
        if keypress in [readchar.key.DOWN, readchar.key.UP]:
            is_yes = not is_yes
            is_selected = True
            current_message = yes_text if is_yes else no_text
        elif keypress in [readchar.key.BACKSPACE, readchar.key.LEFT]:
            if current_message:
                current_message = current_message[:-1]
        elif keypress in [readchar.key.CTRL_C, readchar.key.CTRL_D]:
            abort = True
            break
        elif keypress in [readchar.key.ENTER, readchar.key.RIGHT]:
            if is_selected:
                break
        elif keypress in '\t':
            if is_selected:
                current_message = yes_text if is_yes else no_text
        else:
            current_message += keypress
            match_yes = yes_text
            match_no = no_text
            match_text = current_message
            if not has_to_match_case:
                match_yes = match_yes.upper()
                match_no = match_no.upper()
                match_text = match_text.upper()
            if match_no.startswith(match_text):
                is_selected = True
                is_yes = False
            elif match_yes.startswith(match_text):
                is_selected = True
                is_yes = True
            else:
                is_selected = False
        print()
    print('\033[K\n\033[K\n\033[K\n\033[3A')
    if abort:
        return abort_value
    return is_selected and is_yes



def prompt_min_or_hour(
        question,      # type: str
        min_text = 'Minute',   # type: str
        hour_text = 'Hour',    # type: str
        has_to_match_case = False,    # type: bool  
        enter_empty_confirms = True,  # type: bool
        default_is_min = True,    # type: bool
        deselected_prefix = '  ',  # type: str
        selected_prefix = '\033[31m>\033[0m ', # type: str 
        abort_value = None,     # type: Optional[bool]
        char_prompt = True):    # type: bool
    #type: (...) -> Optional[bool]
    """Prompt the user to input min or hour.

    Args:
        question (str): The prompt asking the user to input.
        min_text (str, optional): The text corresponding to 'min'.
        hour_text (str, optional): The text corresponding to 'hour'.
        has_to_match_case (bool, optional): Does the case have to match.
        enter_empty_confirms (bool, optional): Does enter on empty string work.
        default_is_min (bool, optional): Is yes selected by default (hour).
        deselected_prefix (str, optional): Prefix if something is deselected.
        selected_prefix (str, optional): Prefix if something is selected (> )
        abort_value (bool, optional): The value to return on interrupt.
        char_prompt (bool, optional): Add a [Y/N] to the prompt.

    Returns:
        Optional[bool]: The bool what has been selected.
    """
    is_min = default_is_min
    is_selected = enter_empty_confirms
    current_message = ''
    yn_prompt = ' ({}/{}): '.format(min_text[0], hour_text[0]) if char_prompt else ': '
    abort = False
    lcd = Adafruit_CharLCD.Adafruit_CharLCD()
    selected_prefix_lcd = '> '
    print()

    while True:
    	lcd.clear()
        minute = is_min and is_selected
        hour = not is_min and is_selected
        print('\033[K'
              '{}{}'.format(selected_prefix if minute else deselected_prefix, min_text))
        lcd.message('{}{}\n'.format(selected_prefix_lcd if minute else deselected_prefix, min_text))
        print('\033[K'
              '{}{}'.format(selected_prefix if hour else deselected_prefix, hour_text))
        lcd.message('{}{}\n'.format(selected_prefix_lcd if hour else deselected_prefix, hour_text))
        print('\033[3A\r\033[K'
              '{}{}{}'.format(question, yn_prompt, current_message), end='')
#        lcd.message('{}{}{}'.format(question, yn_prompt, current_message))
        sys.stdout.flush()
        keypress = readchar.readkey()
        if keypress in [readchar.key.DOWN, readchar.key.UP]:
            is_min = not is_min
            is_selected = True
            current_message = min_text if is_min else hour_text
        elif keypress in [readchar.key.BACKSPACE, readchar.key.LEFT]:
            if current_message:
                current_message = current_message[:-1]
        elif keypress in [readchar.key.CTRL_C, readchar.key.CTRL_D]:
            abort = True
            break
        elif keypress in [readchar.key.ENTER]:
            if is_selected:
                break
        elif keypress in '\t':
            if is_selected:
                current_message = min_text if is_min else hour_text
        else:
            current_message += keypress
            match_min = min_text
            match_hour = hour_text
            match_text = current_message
            if not has_to_match_case:
                match_min = match_min.upper()
                match_hour = match_hour.upper()
                match_text = match_text.upper()
            if match_hour.startswith(match_text):
                is_selected = True
                is_min = False
            elif match_min.startswith(match_text):
                is_selected = True
                is_min = True
            else:
                is_selected = False
        print()
    print('\033[K\n\033[K\n\033[K\n\033[3A')
    if abort:
        return abort_value
    return is_selected and is_min


def get_number_arrows(
        prompt,        # type: str
        increment,     # type: int
        max_value,     # type: int
        min_value = 0):     # type: int 
    #type: (...) -> int
    """Get a number from user using arrow keys to increment or decrement. 
    If the starting value 0 is entered prompt user until valid value is entered. 

    Args:
        min_value (int): minimum value inclusive
        max_value (int): maximum value exclusive

    Returns:
        int: number entered by user
    """
    #lcd = Adafruit_CharLCD.Adafruit_CharLCD()

    return_value = -1
    current_value = 0
    max_min_prompt = '({},{}): '.format(str(min_value), str(max_value-1))

    while return_value < min_value:
        print('\n')
        #lcd.clear()
        print('\033[3A\r\033[K'
            '{}{}{}'.format(prompt, max_min_prompt, current_value), end='')
        myLCD.printLine(2, '{}{}{}'.format(prompt, max_min_prompt, current_value))
        #lcd.message('{}{}{}'.format(prompt, max_min_prompt, current_value), line=2)
        #sys.stdout.flush()

        #keypress = readchar.readkey()

        button_pressed = None

        while button_pressed is None:
            getTime()
            button_pressed = wait_for_button()

        #if keypress in [readchar.key.DOWN]:
        if button_pressed == 'down':
            if (current_value - increment) >= min_value:
                current_value -= increment
        #elif keypress in [readchar.key.UP]:
        elif button_pressed == 'up':
            if (current_value + increment) < max_value:
                current_value += increment
        #elif keypress in [readchar.key.ENTER]:
        elif button_pressed == 'green':
            if current_value < max_value and current_value >= min_value:
                return_value = current_value
        #elif keypress in [readchar.key.BACKSPACE]:
        elif button_pressed == 'red':
            return -1
        print()
    print('\033[K\n\033[K\n\033[K\n\033[3A')
    return return_value

