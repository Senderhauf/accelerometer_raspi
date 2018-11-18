from __future__ import print_function
import sys
import getpass


from colorama import init
import readchar

min_value = 0
max_value = 60
prompt = 'Enter duration: '
increment = 5 

return_value = min_value
current_value = return_value
max_min_prompt = ' ({},{}): '.format(str(min_value), str(max_value))
while return_value is 0:
    print('\n')
    print('\033[3A\r\033[K'
        '{}{}{}'.format(prompt, max_min_prompt, current_value), end='')
    sys.stdout.flush()
    
    keypress = readchar.readkey()
    if keypress in [readchar.key.DOWN]:
        if (current_value - increment) > min_value:
            current_value -= increment
    elif keypress in [readchar.key.UP]:
        if (current_value + increment) < max_value:
            current_value += increment
    elif keypress in [readchar.key.ENTER]:
        if current_value < max_value and current_value > min_value:
            return_value = current_value
    print()
print('\033[K\n\033[K\n\033[K\n\033[3A')

print('return value: ' + str(return_value))