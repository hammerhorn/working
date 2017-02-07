#!/usr/bin/env python3
#coding=utf8
"""
Letter Frequency

Generate a table of all the characters used in a text file, sorted according to
their frequency

usage: ./encod_table.py [INPUT_FILE]
"""
import sys

import easycat
from versatiledialogs.terminal import Terminal

def main():
    """Main function"""
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = Terminal.input('Please enter a filename:')
    buf = easycat.cat(files=[filename], quiet=True, return_str=True)
    lines = []
    for char in buf:
        ordinal = ord(char)
        bin_ord = '{0:b}'.format(ordinal).zfill(8)
        if char == '\n':
            char = '\\n'
        lines += ["{:>3}\t{}\t{}".format(ordinal, bin_ord, char)]
    freq = 1
    lines.sort()
    prev_line = lines[0]
    freq_lines = []
    for line in lines[1:]:
        if line == prev_line:
            freq += 1
        else:
            freq_lines += ['{:>3}\t{}'.format(freq, prev_line)]
            freq = 1
        prev_line = line
    if lines[-1] != lines[-2]:
        freq_lines += ['{:>3}\t{}'.format(freq, lines[-1])]
    out_str = ''
    out_str += (
        Terminal.fx('un', 'Frq') +
        '\t' + Terminal.fx('un', 'Ord') +
        '\t' + Terminal.fx('un', 'Bin') +
        '\t\t' + Terminal.fx('un', 'Char') + '\n')
    freq_lines.sort()
    for line in freq_lines:
        out_str += line + '\n'
    easycat.less(out_str)
    Terminal.output('')


Terminal()
if __name__ == '__main__':
    main()
    Terminal.start_app()
