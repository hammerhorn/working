#!/usr/bin/env python
"""
use: vidscript.py ["$URL"]

Framebuffer frontend for youtube.
Also works in X using mplayer.

- fgconsole no longer reveals wheter or not you are in X;
  find a platform-dependent way to do so
- if file already exists (and is complete), you can save time by not downloading
  it
- Also there is no way to predict which frame-buffer driver will work;
  supply an arg
"""
import subprocess
import sys

from cjh.misc import catch_help_flag
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


def get_filename():
    """
    Get filename
    """
    try:
        filename = subprocess.check_output(
            'youtube-dl --get-filename {}'.format(sys.argv[1]), shell=True)
        filename = filename.strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit('{} Unable to locate url: {}.'.format(
            Terminal.fx('bn', 'ERROR:'), sys.argv[1]))
    Terminal.output('Filename: {}\n'.format(filename))
    return filename

def dl_video():
    """
    Download video
    """
    try:
       proc = subprocess.Popen('youtube-dl "{}"'.format(sys.argv[1]), shell=True)
       proc.wait()
    except (OSError, subprocess.CalledProcessError):
        sys.exit('{} Unable to download "{}".'.format(
            Terminal.fx('bn', 'ERROR: '), FILENAME))

def play_video():
    """
    Play video with mplayer, either in X or frame buffer.
    """
    try:
        tty = int(subprocess.check_output('fgconsole'))
        proc = subprocess.Popen(
            'fgconsole 2> /dev/null && ' +
            'mplayer -vo fbdev {0} || mplayer {0}'.format(FILENAME), shell=True)
        proc.wait()

        # on Knoppix, tty1 - tty4 are VTs, tty5 and up are X
        if tty <= LAST_TTY:
            proc = subprocess.Popen(
                'mplayer -vo {} "{}" 2> /dev/null'.format(FB_DRIVER, FILENAME), shell=True)
            proc.wait()
        else:
            proc = subprocess.Popen('mplayer "{}"'.format(FILENAME), shell=True)
            proc.wait()
    except (OSError, subprocess.CalledProcessError):
        sys.exit('{} Unable to play video.'.format(Terminal.fx('bn', 'ERROR')))




FB_DRIVER = 'directfb'
LAST_TTY = 4

def main():
    """
    not sure if it's nessessary to catch both exceptions.
    """
    dl_video()
    play_video()

if __name__ == '__main__':
    catch_help_flag(__doc__, condition=(len(sys.argv[1:]) == 0))
    FILENAME = get_filename()
    main()
