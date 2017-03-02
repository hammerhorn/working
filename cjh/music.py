#!/usr/bin/env python
#coding=utf8
"""
Classes relating to music.
"""
import decimal
import math
import os
import subprocess
import sys
import time

from fiziko.kinematics import Disp, Velocity
from fiziko.scalars import Scalar, Unit
from fiziko.waves import SoundWave
from ranges import gen_range, lst_range
from things import Thing
from versatiledialogs.lists import ItemList
from versatiledialogs.terminal import Terminal


__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

VOL = .01

class Pitch(SoundWave):
    """
    Has attributes like frequency, notename, octave number
    """
    def __init__(self, notename='C', octave=4.0, cents=0.0, freq=None):
        super(Pitch, self).__init__(440)
        self.speed = Velocity(340.29, 'm/s')
        if freq is not None:
            self.set_all_by_freq(float(freq))
        else:
            self.set_all_by_letter(octave, notename, cents)
        self._finish_up()  # Finalize label & set wlength

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __add__(self, float_):
        return Pitch(self.note_name, self.octave, self.cents + (float_) * 100.0)

    def __eq__(self, other):
        """
        True if note is pretty close or to a similar note in a different
        octave
        """
        diff = self.note_float - other.note_float
        cents_diff = self.cents - other.cents
        return -0.25 < diff < 0.25 or\
            (self.note_name == other.note_name and -25 < cents_diff < 25)

    def __ne__(self, other):
        return self.freq != other.freq

    def __ge__(self, other):
        return self.freq >= other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    # Use Property() built-in here
    def set_all_by_freq(self, freq):
        """Seems to work -- 1/25/2015"""
        self.freq = Pitch.yield_freq(freq)
        #Cli.wait(self.freq.__str__())
        #Cli.wait(str(type(self.freq))) Scalar
        #Cli.wait(str(type(self.freq.mag))) Decimal
        self.halfsteps = Pitch.calc_halfsteps(float(self.freq.mag))
        self.local_semitones = Pitch.calc_local_semitones(self.halfsteps)
        self.note_float = Pitch.local2note_float(self.local_semitones)
        self.octave = Pitch.set_oct(freq)
        self.note_number = int(self.note_float)
        self.cents, self.note_number = math.modf(self.note_float)
        self.cents *= 100.0
        self.octave, self.note_number, self.cents = self.round((
            self.octave, self.note_number, self.cents))
        self.reset_number_name_oct(self.note_float, self.freq)

    def set_all_by_letter(self, octave, notename='C', cents=0.0):
        """Seems to work -- 1/25/2015"""
        self.octave, self.note_name, self.cents =\
            Pitch._digest_notename(octave, notename, cents)
        self.note_number = Pitch.letter2number(self.note_name)
        self.note_float = self.note_number + (self.cents / 100.0)
        self.halfsteps = Pitch.calc_halfsteps((self.note_float, self.octave))
        note_tuple = (self.octave, self.note_number, self.cents)
        self.freq = Pitch.yield_freq(note_tuple)
        self.local_semitones = Pitch.calc_local_semitones(self.halfsteps)
        self._finish_up()

    @staticmethod
    def _digest_notename(octave, note_name, cents):
        """
        Format notename; set note_number, note_float, and convert to
        simplest form.  This should be made to use recursion.
        """
        note_number = Pitch.letter2number(note_name)
        note_name = Pitch.number2letter(note_number)
        octave, note_name, cents = Pitch.round((octave, note_number, cents))
        return (octave, note_name, cents)

    @staticmethod
    def round(note_tuple):
        """
        Takes tuple(octave, note_number, cents).
        If cents < -50 or cents > 50, simplify.
        """
        octave, note_number, cents = note_tuple
        note_float = note_number + (float(cents) / 100.0)
        cents, note_number = math.modf(note_float)
        cents *= 100.0
        octave = float(octave)

        if cents >= 50.0:
            cents -= 100.0
            note_float += 1.0
            note_number = int(note_float)
            notename = Pitch.number2letter(note_number)
            if notename == 'C':
                octave += 1.0
        elif cents < -50.0:
            cents += 100.0
            note_float -= 1.0
            note_number = int(note_float)
            notename = Pitch.number2letter(note_number)
            if notename == 'B':
                octave -= 1.0
        else:
            notename = Pitch.number2letter(int(note_float))

        if note_float >= 12.0:
            note_float -= 12
            octave += 1.0
        elif note_float < 0.0:
            note_float += 12.0
            octave -= 1.0
        return (octave, notename, cents)

    @staticmethod
    def letter2number(nname):
        """
        Takes a notename in rough form and outputs the int note_number
        """
        if nname in ('A#', 'a#', 'Bb', 'bb', 'A♯/B♭'):
            number = 1
        elif nname in ('B', 'b'):
            number = 2
        elif nname in ('C', 'c'):
            number = 3
        elif nname in ('C#', 'c#', 'Db', 'db', 'C♯/D♭'):
            number = 4
        elif nname in ('D', 'd'):
            number = 5
        elif nname in ('D#', 'd#', 'Eb', 'eb', 'D♯/E♭'):
            number = 6
        elif nname in ('E', 'e', 'Fb', 'fb'):
            number = 7
        elif nname in ('F', 'f', 'E#', 'e#'):
            number = 8
        elif nname in ('F#', 'f#', 'Gb', 'gb', 'F♯/G♭'):
            number = 9
        elif nname in ('G', 'g'):
            number = 10
        elif nname in ('G#', 'g#', 'Ab', 'ab', 'G♯/A♭'):
            number = 11
        elif nname in ('a', 'A'):
            number = 0
        else:
            Terminal.output('ERROR -- Invalid notename.')
            number = -1
        return number

    @staticmethod
    def number2letter(number):
        """
        Converts int note_number to polished notename
        """
        if number >= 12:
            number -= 12
        pattern = (0, 2, 3, 5, 7, 8, 10)
        if number in pattern:
            letter = chr(pattern.index(number) + 65)

        note_dict = {
            1: 'A♯/B♭',
            4: 'C♯/D♭',
            6: 'D♯/E♭',
            9: 'F♯/G♭',
            11: 'G♯/A♭'}

        return note_dict.get(number, -1)


    @staticmethod
    def local2note_float(local):
        """
        Both local and note_float are measured from A==0, but
        -6 <= local <= 6, whereas 0 <= note_float < 12
        """
        note_float = local
        while note_float < 0:
            note_float += 12.0
        return note_float

    @staticmethod
    def calc_local_semitones(halfsteps):
        """
        When you know 'halfsteps' in relationship to A440,
        you can find the distance in semitones to the closest A, i.e.,
        'local_semitones'.
        """
        local_semitones = halfsteps % 12 #; //HSs + or - A in this octave
        if local_semitones < -6.0:
            local_semitones += 12.0
        elif local_semitones >= 6.0:
            local_semitones = -1.0 * (12.0 - local_semitones)
        return local_semitones

    @staticmethod
    def calc_halfsteps(param):
        """
        Takes either a float frequency or a tuple(float octave,
        float note_float)
        """
        if type(param) == float or type(param) == int:
            halfsteps = 12.0 * math.log(param / 440.0) / math.log(2.0)

        elif type(param) == tuple:
            octave, note_float = param
            note_float = float(note_float)
            halfsteps = note_float + (octave - 5) * 12.0
            num = int(note_float)
            if num in (0, 1, 2):
                halfsteps += 12
        else:
            sys.exit('error')#return None
        return halfsteps

    @staticmethod
    def calc_freq(octave, note_float):
        octave = float(octave)
        note_float = float(note_float)
        c1_freq = 32.70319566257483
        freq_float = c1_freq * 2.0 ** ((note_float - 3.0) / 12.0) * 2.0 ** (
            octave - 1.0)
        freq_scalar = Scalar(freq_float, Unit('Hz'))
        num = int(note_float)
        if num in (0, 1, 2):
            freq_scalar.mag *= decimal.Decimal(2.0)
        return freq_scalar

    @staticmethod
    def set_oct(freq):
        """
        Determines the octave of a frequency
        """
        return int(math.log((float(freq) / 15.886), 2))

    def _finish_up(self):
        """
        1)format cents string for label,
        2)set label, and
        3)set wlength
        """
        # 1)
        cents_str = '%+5.2f' % (self.cents / 100.0)
        cents_str = cents_str[0] + cents_str[2:]

        # 2)
        self.label = '{}{} ({})'.format(
            self.note_name, int(self.octave), cents_str)

        # 3)
        #(fix this)       self.wlength = Disp(self.speed.mag / self.freq.mag)
        self.wlength = Disp(self.speed.mag / self.freq.mag)
        if self.note_name in ('A', 'A♯/B♭', 'B'):
            self.wlength.mag /= 2

    def reset_number_name_oct(self, note_float, freq):
        """
        Resets note_number, note_name, and octave
        """
        self.note_number = round(note_float)
        self.note_name = Pitch.number2letter(self.note_number)
        self.octave = Pitch.set_oct(freq.mag)


    @staticmethod
    def yield_freq(param):
        """
        param is a number freq or a tuple (oct, number, cents); returns a Scalar
        in Hz.
        """
        if type(param) == int or type(param) == float:
            return Scalar(param, Unit('Hz'))
        else:
            octave, note_num, cents = param
            note_num = float(note_num)
            cents = float(cents)
            note_float = note_num + (cents / 100.0)
            return Pitch.calc_freq(octave, note_float)


    def halfsteps_info(self):
        """should this be a template?"""
        return '{:.3} half-steps above A440\n{:.3} half-steps above the nearest A\n'.format(
            self.halfsteps, self.local_semitones)


    def __str__(self):
        return '{:>13}\t{}'.format(self.label, self.freq)

    def details(self):
        # ItemList currently does not support labels lol
        string = '\n  {}'.format(
            Terminal.fx('un', ''.join(('  ', self.label, ' ' * 26))))
        string += ItemList(
            [self.freq] + self.halfsteps_info().split('\n')[:-1],
            self.label).__str__()
        return string

    def play(self, voice='squ'):
        """
        Currently uses a system call to sox
        """
        NOTE_LENGTH = .15 #.1
        command = 'play -n synth {} {} {} vol {} > /dev/null 2>&1'.format(
            NOTE_LENGTH, voice, self.freq.mag, VOL)
        proc = subprocess.Popen(command, shell=True)
        proc.wait()


class Note(Pitch):
    """
    a Pitch with a duration    """
    def __init__(self, a_pitch, duration):
        self.speed = Velocity(340.29, 'm/s')
        self.octave = a_pitch.octave
        self.cents = a_pitch.cents
        self.note_name = a_pitch.note_name
        self.note_float = a_pitch.note_float
        self.freq = a_pitch.freq
        self.halfsteps = a_pitch.halfsteps
        self.local_semitones = a_pitch.local_semitones
        self.duration = duration
        self.label = a_pitch.label

#    def __str__(self):
#        string = '\n{}\n'.format(Cli.term_fx('un', self.label))
#        string += '{}\n'.format(self.freq)
#        string += self.halfsteps_info()
#        return string

    def play(self, voice='tri'):
        """
        Currently uses a system call to sox
        """
        proc = subprocess.Popen('play -n synth {} {} {} vol {} > /dev/null 2>&1'.format(
            self.duration, voice, self.freq.mag, VOL), shell=True)
        proc.wait()


class PitchSet(Thing):
    """
    defines a key or harmonic mode
    """
    def __init__(self, et=12, pattern=None, start_pitch=Pitch('C', 3)):
        """
        'pattern' is list which acts as a filter, e.g.,
        [1, 3, 5, 6, 8, 10, 12] would define the diatonic scale.
        """
        super(PitchSet, self).__init__()
        self.label = 'PitchSet #{}'.format(PitchSet.count)
        if pattern is None:
            pattern = lst_range(1, int(et+1))
        #else:
        #    pattern =
        #    pattern = [ int(i) for i in pattern ]
        #self.pitches = []
        if 1 in pattern:
            self.pitches = [start_pitch]
            del pattern[pattern.index(1)]
        else:
            self.pitches = []
        for x in gen_range(int(et) - 1):
            if x + 2 in pattern:
                f = float(start_pitch.freq.mag) * 2 ** ((x + 1) / float(et))
                self.pitches.append(Pitch(freq=f))

    def __str__(self):
        out_str_list = ['\n']
        for pitch in self.pitches:
            if len(pitch.label) > 9:
                out_str_list.append('{:>19}\n'.format(pitch.label))
            else:
                out_str_list.append('{:>15}\n'.format(pitch.label))
        return ''.join(out_str_list)

    def __getitem__(self, index):
        return self.pitches[index]

    def play(self, voice='sin'):
        Note(self.pitches[0], .05).play()
        time.sleep(.03)
        for x in gen_range(int((20 + len(self.pitches)) / len(self.pitches))):
            for pitch in self.pitches[1:]:
                Note(pitch, .05).play(voice)
                time.sleep(.03)
            #for pitch in self.pitches[:-1][::-1]:
            for pitch in reversed(self.pitches[:-1]):
                Note(pitch, .05).play(voice)
                time.sleep(.03)

    def play_chord(self, wform='pl'):
        """
        Currently uses a system call to sox
        """
        NOTE_LENGTH = 1
        command_list = ['play -n synth {} '.format(NOTE_LENGTH)]
        for pitch in self.pitches:
            command_list.append('{} {:.4g}{}'.format(wform, pitch.freq.mag, ' '))
        command_list.append('vol {} > /dev/null 2>&1'.format(VOL))
        command = ''.join(command_list)
        proc = subprocess.Popen(command, shell=True)
        proc.wait()


class PitchSequence(Thing):

    def __init__(self, pitch_set=PitchSet(pattern=[1, 3, 5, 6, 8, 10, 12]),
                 seq=(1, 1, 5, 5, 6, 6, 5)):

        super(PitchSequence, self).__init__()

        self.p_seq = []
        for x in seq:
            self.p_seq.append(pitch_set[x - 1])

    def play(self):
        for pitch in self.p_seq:
            pitch.play()

    def __getitem__(self, index):
        return self.p_seq[index]

    def __str__(self):
        return self.p_seq.__str__()

    def __len__(self):
        return len(self.p_seq)

    def pprint(self):
        out_str_list = []
        for x in self.p_seq:
            out_str_list.append(x.__str__())
        Terminal.output('\n%s\n' % '\n'.join(out_str_list))
