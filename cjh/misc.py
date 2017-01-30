#!/usr/bin/env python
#coding=utf8
"""
contains: bye(),
          chomp(text),
          color_dec_to_hex(r, g, b),
          current_time()
          fahr_to_kelvins(fahr),
          help_dialog(),
          speak()
"""
import datetime
import os
import subprocess
import sys
# import time


from versatiledialogs.terminal import Terminal

# from colorful import color
# from cjh.music import PitchSequence, PitchSet, Pitch

         
def bye():
    """
    Marks the end of the program.  Maybe it could be moved to <cjh.shell.Cli>.
    """
    # vt.Terminal.output('Bye.')
    # PitchSequence(PitchSet(pattern=[1, 3, 5, 6, 8, 10, 12], start_pitch=Pitch('C', 4)), [5, 1]).play()
    sys.exit('\nBye.')
    


def catch_help_flag(help_str, sh_obj=Terminal(), condition=None, cleanup=lambda:0):
    """
    Help dialogs for bash and Tk.
    """
    if {'-h', '--help'} & set(sys.argv) or condition is True:
        #sh_obj.output(__doc__[1:])
        #                    sys.exit(0)
        module = sys.argv[0].replace('./', '')[:-3]
        if sh_obj.interface == 'Tk':
        #sh_obj.main_window.title(module)
            sh_obj.message(help_str, module)
        else:
            module = "'{}'".format(module.replace('_', ' ').title())
            Terminal.output(Terminal.ul(module, position=1))
            sh_obj.output(help_str + '\n')
        cleanup()
        if sh_obj.interface == 'Tk':
            sh_obj.main_window.destroy()
        sys.exit()
                
def chomp(text):
    text = text.replace('\n', ' ')
    text = text.strip()
    return text
    

def current_time():
    today = datetime.datetime.today()
    return today.strftime('%l:%M:%S %P')


def fahr_to_kelvins(fahr):
    celsius = (fahr - 32) * 5.0 / 9.0
    kelvins = celsius + 273.15
    return kelvins

def notebook(remarks):
    if '-C' in sys.argv[1:]:
        Terminal()
        if Terminal.os_name == 'posix' and 'DISPLAY' in os.environ:
            remarks = remarks.replace('    *', '    •')
            if Terminal.platform == 'Linux':
                remarks = remarks.replace('    -', '    ☐')
                remarks = remarks.replace('    +', '    ☒')
        else:
            remarks = remarks.replace('    -', '    [ ]')
            remarks = remarks.replace('    +', '    [x]')

        Terminal.clear()
        heading = sys.argv[0]
        if '/' in heading:
            heading = heading.split('/')[1]
        heading = 'Module: ' + heading[:-3]
        Terminal.print_header(message=heading)
        Terminal.output('{}'.format(remarks))
        Terminal.wait()
        Terminal.output('')
        sys.exit(0)

def speak(phrase):
    command = 'espeak -s 150 -v en-us -p 30 "{}" > /dev/null 2>&1'
    try:
        proc = subprocess.Popen(command.format(phrase), shell=True)
        proc.wait()
    except:
        raise
        Terminal.notify('espeak failed')
                        
