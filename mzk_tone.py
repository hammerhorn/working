#!/usr/bin/env python
#coding=utf8
"""
Play one musical tone.

./mzk_tone.py $freq
./mzk_tone.py $notename [$octave [$cents]]
"""
import sys

from cjh.misc import catch_help_flag, notebook
from cjh.music import Pitch

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    - B4 and B4+.50 should not be an octave apart
    - Cb and B# should not be invalid note names

    * German-style and Latin-style notenames
    * There should be a random note feature"""

if __name__ == '__main__':
    notebook(REMARKS)
    catch_help_flag(__doc__)
    if len(sys.argv[1:]) >= 1 and sys.argv[1].replace('.', '', 1).isdigit():
        TONE = Pitch(freq=sys.argv[1])
    elif len(sys.argv[1:]) == 1:
        TONE = Pitch(sys.argv[1])
    elif len(sys.argv[1:]) == 2:
        TONE = Pitch(sys.argv[1], sys.argv[2])
    elif len(sys.argv[1:]) == 3:
        TONE = Pitch(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        TONE = Pitch()

    print('{:.7} {}={}'.format(
        TONE.freq.mag, TONE.freq.units.abbrev, TONE.label))
    TONE.play()
