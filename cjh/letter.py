#coding=utf8
import time
from cjh.music import Pitch, Note
from cjh.misc import speak
"""
translate the Roman alphabet into, e.g.,
radiophonic words, morse code, braille, etc....
"""

class Letter(object):
    """
    convert between different forms of Roman-alphabet letters
    """
    morse_dict = {
        '1':'.----',
        '2':'..---',
        '3':'...--',
        '4':'....-',
        '5':'.....',
        '6':'-....',
        '7':'--...',
        '8':'---..',
        '9':'----.',
        '0':'-----',
        'A':'.-',
        'B':'-...',
        'C':'-.-.',
        'D':'-..',
        'E':'.',
        'F':'..-.',
        'G':'--.',
        'H':'....',
        'I':'..',
        'J':'.---',
        'K':'-.-',
        'L':'.-..',
        'M':'--',
        'N':'-.',
        'O':'---',
        'P':'.--.',
        'Q':'--.-',
        'R':'.-.',
        'S':'...',
        'T':'-',
        'U':'..-',
        'V':'...-',
        'W':'.--',
        'X':'-..-',
        'Y':'-.--',
        'Z':'--..',
        ' ':'/', '.':'.-.-.-'}

    radio_dict = {
        'A':'Alfa',
        'B':'Bravo',
        'C':'Charlie',
        'D':'Delta',
        'E':'Echo',
        'F':'Foxtrot',
        'G':'Golf',
        'H':'Hotel',
        'I':'India',
        'J':'Juliett',
        'K':'Kilo',
        'L':'Lima',
        'M':'Mike',
        'N':'November',
        'O':'Oscar',
        'P':'Papa',
        'Q':'Quebec',
        'R':'Romeo',
        'S':'Sierra',
        'T':'Tango',
        'U':'Uniform',
        'V':'Victor',
        'W':'Whiskey',
        'X':'Xray',
        'Y':'Yankee',
        'Z':'Zulu', ' ':None, '.':None}


    braille_dict = {
        'A':'⠁',
        'B':'⠃',
        'C':'⠉',
        'D':'⠙',
        'E':'⠑',
        'F':'⠋',
        'G':'⠛',
        'H':'⠓',
        'I':'⠊',
        'J':'⠚',
        'K':'⠅',
        'L':'⠇',
        'M':'⠍',
        'N':'⠝',
        'O':'⠕',
        'P':'⠏',
        'Q':'⠟',
        'R':'⠗',
        'S':'⠎',
        'T':'⠞',
        'U':'⠥',
        'V':'⠧',
        'W':'⠺',
        'X':'⠭',
        'Y':'⠽',
        'Z':'⠵', ' ':None, '.':None}

    def __init__(self, char):
        self.majuscule = char.upper()
        self.radio_name = self.__class__.radio_dict[char.upper()]
        self.braille = self.__class__.braille_dict[char.upper()]
        self.morse = self.__class__.morse_dict[char.upper()]
        self.mora = 0.125
        self.wpm = 1.2 / self.mora
        self.hz = 1000
        
    def __str__(self):
        return '{} {} {}'.format(self.radio_name, self.braille, self.morse)

    def play_morse(self):
        for x in self.morse:
            if x == '.':
                Note(Pitch(freq=self.hz), self.mora).play()
                #time.sleep(.025)
            elif x == '-':
                Note(Pitch(freq=self.hz), self.mora * 3).play()
            elif x == ' ':
                time.sleep(7 * self.mora)
            time.sleep(self.mora)
        time.sleep(3 * self.mora)

    def radio_speak(self):
        spoken_forms = {
            'J': 'Julie-et',
            'O': 'Oska',
            'P': 'Pawpaw',
            'Q': 'Kebec'
            }
        speak(spoken_forms.get(self.majuscle, self.radio_name))

