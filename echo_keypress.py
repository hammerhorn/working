#!/usr/bin/env python3
"""
output the corresponding ordinal value for the pressed key character
"""
from easycat import write
from versatiledialogs.terminal import Terminal

Terminal()

def main():
    """Main function"""
    while True:
        prest = Terminal.get_keypress()
        write(Terminal.fx('un', str(ord(prest))) + ' ')

if __name__ == '__main__':
    main()
