from blessed import Terminal
from blessed.keyboard import Keystroke
term = Terminal()
with term.cbreak():
    val = Keystroke('')
    query = ''
    while val.is_sequence != True and val.name !='KEY_ENTER':
        val = term.inkey()
        if val.is_sequence:
            pass
        elif val:
           print("got {0}.".format(val))
           query += val
    print(query)
    print(f'bye!{term.normal}')
