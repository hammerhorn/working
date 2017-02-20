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
import argparse
import datetime
import json
import os
import subprocess
import sys

from versatiledialogs.terminal import Terminal


def bye():
    """
    Marks the end of the program.  Maybe it could be moved to <cjh.shell.Cli>.
    """
    # vt.Terminal.output('Bye.')
    # PitchSequence(PitchSet(pattern=[1, 3, 5, 6, 8, 10, 12], start_pitch=Pitch\
    # ('C', 4)), [5, 1]).play()
    sys.exit('\nBye.')


def catch_help_flag(help_str='', sh_obj=Terminal(), condition=None,
                    cleanup=None, # a function to end with
                    module=sys.argv[0].replace('./', '').split('.')[0],
                    argprsr=None): # an argparse.parser
    """
    Help dialogs for bash and Tk.
    """
    if {'-h', '--help'} & set(sys.argv) or condition is True:
        #sh_obj.output(__doc__[1:])
        #                    sys.exit(0)
        #module = heading
        if sh_obj.interface == 'Tk':
        #sh_obj.main_window.title(module)
            sh_obj.message(msg=help_str, heading=module)
        else:
            module = module.replace('_', ' ').title()
            #Terminal.output(Terminal.ul(module, position=1))
            Terminal.output('\n' + Terminal.fx('bnu', module))
            sh_obj.output(help_str)
            sys.argv.append('-h')
            #parser = argparse.ArgumentParser()
            try:
                if argprsr is not None:
                    argprsr.parse_args()
            finally:
                Terminal.output('')
        if cleanup is None:
            cleanup = sh_obj.exit
        cleanup()
#        if sh_obj.interface == 'Tk':
#            sh_obj.main_window.destroy()
#        sys.exit()


def chomp(text):
    """removes trailing whitespace, turns internal newlines into spaces"""
    text = text.replace('\n', ' ').strip()
    #text = text.strip()
    return text


def current_time():
    """returns the current time as a formatted str"""
    today = datetime.datetime.today()
    return today.strftime('%l:%M:%S %P')


def fahr_to_kelvins(fahr):
    """converts Fahrenheit to Kelvin; move this to fiziko lib"""
    celsius = (fahr - 32) * 5.0 / 9.0
    kelvins = celsius + 273.15
    return kelvins


def notebook(remarks):
    """
    My personal notekeeping system; type -C after a command to reach the
    notebook.
    """
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

def read_json_file(filename):
    file_ptr = open(filename, 'rb')  # binary?  really?
    buffer_ = file_ptr.read().decode('utf-8')
    return json.loads(buffer_)
            

def speak(phrase):
    """use a speech synthesizer to read text"""
    command = 'espeak -s 150 -v en-us -p 30 "{}" > /dev/null 2>&1'
#   try:
    proc = subprocess.Popen(command.format(phrase), shell=True)
    proc.wait()
#   except:
#        Terminal.notify('espeak failed')

