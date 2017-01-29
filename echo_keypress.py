#!/usr/bin/env python
from easycat import write
from versatiledialogs.terminal import Terminal

Terminal()
while True:
    prest = Terminal.get_keypress()
    write(Terminal.fx('un', str(ord(prest))))
    write(' ')
