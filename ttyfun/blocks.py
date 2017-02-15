#!/usr/bin/env python
import time
from versatiledialogs.terminal import Terminal
import easycat

from ranges import gen_range

def box(msg, symbol='*', position=None, width=None):
    """
    Print a one-line string surrounded by a border; 'symbol' keyword
    defines the str used for drawing the border, '*' is default; if
    'position' keyword >= 0, banner will be left-aligned and indented
    int 'position' spaces.  if 'position' keyword < 0 or is unused,
    banner will be centered and moved to the left by abs(position) no.
    of spaces.
    """
        #msg = str(msg)  # .decode('utf8')
        #msg = unicode(msg)  #msg = msg.decode('utf-8')
        #msg = codecs.decode(msg, 'utf8')
    Terminal()        
    banner_width = len(msg) + 2 * (len(symbol) + 1)
    
    column_total = width if width is not None else Terminal.width()
    content = '\n'
    star_bar = (symbol * (banner_width // len(symbol)))
    # sym_gen = iter(symbol)
    # while len(star_bar) < banner_width:
    #     star_bar += next(sym_gen)  # sym_gen.next()
    padding = ' '
    messagef = ''.join((symbol, padding, msg, padding, symbol))

    if position is None or position < 0:
        if position is None:
            position = 0
        column_total += (2 * position)
        star_bar = star_bar.center(column_total)
        messagef = messagef.center(column_total)
    else:
        indent_pad = ' ' * position
        star_bar = indent_pad + star_bar
        messagef = indent_pad + messagef

    star_bar += '\n'
    messagef += '\n'
    content = ''.join((content, star_bar, messagef, star_bar))
    return content
    
def ellipses(msg, iters=3, restore_cursor=True):
    """
    Print message to stdout followed by an animated '....'.
    """
    Terminal()
    easycat.write(msg)
    easycat.write('...')
    delta_t = 0.125
    #iters = repeat
    try:
        Terminal.hide_cursor()
        for _ in gen_range(iters):
            time.sleep(delta_t)
            Terminal.cursor_h(-3, ' ')
            Terminal.cursor_h(2, '.')

            time.sleep(delta_t)
            Terminal.cursor_h(-4, '. .')

            time.sleep(delta_t)
            Terminal.cursor_h(-2, '. ')

            time.sleep(delta_t)

            Terminal.cursor_h(-1, '. ')
            Terminal.cursor_h(-1)
    finally:
        if restore_cursor is True:
            Terminal.unhide_cursor()
