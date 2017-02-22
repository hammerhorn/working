
#!/usr/bin/env python3
"""
Read from command line args or stdin, converting to Morse code.
"""
import atexit
import getpass
import sys
import time

from cjh.letter import Letter
from cjh.misc import notebook
import easycat
from versatiledialogs.terminal import Terminal


REMARKS = """
    - figure out multitasking
    - there is a problem with some soundcards which necessitates very
      slow timing
    - add Tk
    + build it into the letter object"""

Terminal()
notebook(REMARKS)

def play_and_print(char):
    """
    write dots and dashes while also playing audible Morse code sounds
    """
    try:
        letter = Letter(char)
        easycat.write(Terminal.fx('bn', letter.morse + ' '))
        letter.play_morse()
    except KeyError:
        #make it flash?
        time.sleep(.1)
        easycat.write(char)

def main():
    """
    main
    """
    during_input = False
    def siggie():
        Terminal.cursor_v(-1)
        Terminal.clear(0)
        if during_input is True or len(sys.argv[1:]) > 0:
            Terminal.output('\n' * 2 +
                ' '.join(('#',) * 4).center(Terminal.width()))
            Terminal.hrule()
            Terminal.output('')

    atexit.register(siggie)
    atexit.register(Terminal.unhide_cursor)

    Terminal.hide_cursor()
    sample = Letter(' ')
    Terminal.print_header('{} Hz, {} words per minute'.format(
        sample.hz, sample.wpm))

    if len(sys.argv[1:]) > 0:
        easycat.write('    ')
        char_string = sys.argv[1].upper()
        for char in char_string:
            play_and_print(char)
    else:
        line_no = 1

        try:
            while True:
                during_input = True
                line = Terminal.input(
                    prompt='%2d: ' % line_no, hide_form=True)
                Terminal.cursor_v(1)
                during_input = False
                if line == 'END':
                    break
                easycat.write('\t')

                for char in line:
                    play_and_print(char)
                Terminal.output('')
                line_no += 1

        except KeyboardInterrupt:
            Terminal.output('')


if __name__ == '__main__':
    main()
    Terminal.start_app()
