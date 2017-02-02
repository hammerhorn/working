#!/usr/bin/env python
#coding=utf8
"""
Contains Tonerow class.

Ought to be merged with <cjh.music> module
"""
import random
import subprocess

from termcolor import colored

from cjh.music import Pitch, PitchSequence, PitchSet
from ranges import gen_range, lst_range
from things import Thing
from versatiledialogs.terminal import Terminal

class Tonerow(Thing):
    """
    A shuffled, equal-tempered sequence in which each tone is used exactly once;
    It really ought to inherit from pitchsequence, but fuck it
    """
    def __init__(self, length=12, int_list=None, sh_obj=Terminal()):
        #self.gen_range = range(length) if Terminal.py_version == 3 else xrange(length)
        #self.lst_range = list(range(length)) if Terminal.py_version == 3 else range(length)        
        super(Tonerow, self).__init__()
        # sh_obj should belong to Thing
        self.sh_obj = sh_obj
        if int_list is not None:
            self.seq = int_list
        else:
            Terminal()

            # Time some of these constructions
            self.seq = lst_range(length)  # list(range(length)) if Terminal.py_version == 3 else\
                       #range(length)

            index = length - 1
            #itrbl = range(length) if Terminal.py_version == 3 else xrange(length)
            for count in gen_range(length):  # itrbl:
                max_index = index - count
                random_index = random.randint(0, max_index)
                self.seq[max_index], self.seq[random_index] =\
                    self.seq[random_index], self.seq[max_index]

        self.pseq = PitchSequence(PitchSet(len(self)), [i + 1 for i in self.seq])
        self.basename = self.generate_basename()

    def __str__(self):
        return str(self.seq).replace('[', '').replace(']', '').replace(',', '')

    def __len__(self):
        return len(self.seq)

    def __getitem__(self, index):
        return self.pseq[index]

    def draw_list_play(self):
        """
        draw, list, play
        """
        self.draw()
        self.listfreqs()
        self.write_abc_file()
        #self.plot()
        #self.play()

    def play(self):
        """
        play tonerow
        """
        self.pseq.play()



    def plot(self):
        """
        plot tonerow contour with matplotlib
        """
        import matplotlib.pyplot as plt
        Terminal.output('\nClose Pyplot window to continue....')
        plt.axis([-0.2, len(self) - 0.8, -0.2, len(self) - 0.8])
        plt.plot(lst_range(len(self)), self.seq, 's--')  # , ms=10.0)
        plt.show()  # list/range -- edit this

    def draw(self, get_str=False):#, shell_name='bash'):
        """
        draw tonerow diagram
        """
        out_str = '\n\n '
        maximum = len(self)
        if maximum < 12:
            out_str += ' '
        out_str += str(self.seq)

        hrule_width = int(round(2.91666 * maximum)) + 7
        if self.sh_obj.interface == 'Tk':
            hrule_width = int(hrule_width * 0.55)
        out_str += '\n' + '=' * (hrule_width) + '\n'

        out_str += '\n'

        #gen_rng = range(maximum) if Terminal.py_version == 3 else xrange(maximum)
        for row in gen_range(maximum):
            str_row = ' {:>2} '.format(maximum - row - 1)
            for index in gen_range(maximum):
                if self.seq[index] == maximum - row - 1:
                    if self.sh_obj.interface == 'term':
                        if self.sh_obj.os_name == 'posix':
                            str_row += colored('   ', attrs=['reverse', 'bold'])
                        else:
                            str_row += colored('   ', 'white', 'on_white')
                    else:
                        str_row += '[*]'
                else:
                    str_row += '. .'
            out_str += str_row + '\n'
        out_str += '\n'
        if get_str is True:
            return out_str
        else:
            if self.sh_obj.interface == 'dialog':
                wide, high = 46, 24
            elif self.sh_obj.interface == 'Tk':
                wide, high = 400, 300
            else:
                wide, high = None, None
            self.sh_obj.output(out_str, width=wide, height=high)

    def reverse(self):
        """
        reverse the tonerow in place
        """
        self.seq = self.seq[::-1]
        self.pseq = PitchSequence(
            PitchSet(len(self), start_pitch=self.get_lowest_tone()), [i + 1 for i in self.seq])

    def invert(self):
        """
        inverts hi with lo tones (in place)
        """
        self.seq = [len(self) - i - 1 for i in self.seq]
        self.pseq = PitchSequence(
            PitchSet(len(self), start_pitch=self.get_lowest_tone()), [i + 1 for i in self.seq])


    def rotate(self):
        """
        rotate
        """
        backup = tuple(self.seq)
        for outer, _ in enumerate(backup):
            for inner, _ in enumerate(backup):
                if backup[inner] == outer:
                    self.seq[outer] = len(backup) - inner - 1
        self.pseq = PitchSequence(
            PitchSet(len(self), start_pitch=self.get_lowest_tone()), self.seq)

    def transpose(self, interval):
        """
        transpose the row by an interval up or down
        """
        #freqs = [i.freq.mag for i in self.pseq]
        #min_freq = min(freqs)
        p_set = PitchSet(len(self), start_pitch=self.get_lowest_tone() + interval)
        self.pseq = PitchSequence(p_set, seq=[i + 1 for i in self.seq])
        #for x in range(len(self.pseq)):
        #    self.pseq[x] += interval
#        self.seq = [i + interval for i in self.seq]
#        self.pseq = PitchSequence(PitchSet(), self.seq)
#        self.draw_list_play()


    def get_lowest_tone(self):
        """
        return the lowest-pitched Pitch in this Tonerow - this should be an attribute
        """
        freqs = [i.freq.mag for i in self.pseq]
        min_freq = min(freqs)
        return Pitch(freq=min_freq)

    def listfreqs(self, get_str=False):
        """
        print the notenames and frequencies of the row's tones
        """
        out_str = ''
        for pitch in self.pseq:
            out_str += '\t{}\n'.format(pitch.__str__())
        if get_str is True:
            return out_str
        else:
            Terminal.output(out_str)

    def generate_abc_str(self):
        """return ABC notation as a string"""
        abc_list = []
        for tone in self:
            if len(tone.note_name) == 1:
                abc_list += ['=' + tone.note_name + ' ']
            else:
                abc_list += ['^' + tone.note_name[0] + ' ']
        out_str = """X: 1
T: {}
C:
M: {}/4
L: 1/4
K: C
""".format(self.label, len(self))
        count = 0
        for i in abc_list:
            out_str += i
            count += 1
#            if count < len(self) and count % 4 == 0:
#                out_str += '| '
        out_str += '|]\n'
        return out_str

#    def write_abc(self):
#        """
#        Convert to ABC notation, and then on to postscript sheet music and midi#;
#        display the postscript staff notation and play MIDI audio.
#        """

#    def generate_random_basename(self):
#        """
#        compare TextGen
#        """
#        str_length = 10
#        basename = ''.join(
#            random.choice(
#               string.ascii_lowercase) for _ in range(str_length))
#        return basename

    def generate_basename(self):
        """
        Convert sequence to hex and this will be the basename
        """
        basename = ''
        for i in self.seq:
            #print i
            #Cli.wait(i)
            basename += hex(i)[2:].upper()
        return basename



    def play_midi(self, player='timidity'):
        """
        Play midi file with designated player, timidity by default
        """
        proc = subprocess.Popen((
            'abc2midi __data__/{0}.abc -Q 140 > /dev/null &&' +
            ' {1} __data__/{0}1.mid > /dev/null&').format(self.basename, player), shell=True)
        proc.wait()



    def write_abc_file(self):
        """write ABC data to a file"""
        abc_str = self.generate_abc_str()
        filename = '__data__/' + self.generate_basename() + '.abc'
        handler = open(filename, 'w')
        handler.write(abc_str)
        handler.close()
        Terminal.notify("'{}' written".format(filename))


#        basename = generate_basename()
#        write_abc_file(basename)
        #kpress = Cli.get_keypress("write to abc file '{}'?".format(filename
            #))

            #if kpress in 'Yy':
# ? is this needed?            if True:
                #print abc_str
        #filename = Cli().input('filename(.abc): ')
        #if filename.endswith('.abc'):
        #    filename = filename[:-4]
        #Cli.clear(1)
#       filename += '.abc'
#       Cli.output('filename(.abc): {}'.format(filename))
        #filename = ''


        #cli.less(file_=filename)

        #Cli()

        #Cli.output(abc_str)

#        abc2postscript(basename)


        #Cli.wait()


    def abc2postscript(self):#
        """ use system calls to generate postscript
            and display it """
        #filename = filename.split('.')[0]
        basename = self.generate_basename()
        proc = subprocess.Popen((
            'yaps __data__/{0}.abc > /dev/null &&' +
            ' evince __data__/{0}.ps 2> /dev/null&').format(basename), shell=True)
        proc.wait()

    def shift_h(self, cols):
        """
        shift horizontally
        """
        if cols >= 0:
            for _ in gen_range(cols):
                self.seq = [self.seq[-1]] + self.seq[:-1]
        else:
            for _ in gen_range(abs(cols)):
                self.seq = self.seq[1:] + [self.seq[0]]

    def shift_v(self, rows):
        """
        shift vertically
        """
        for index in gen_range(len(self)):  # for tone in self:?
            self.seq[index] = self.seq[index] + rows
            if self.seq[index] >= len(self):
                self.seq[index] -= len(self)
            elif self.seq[index] < 0:
                self.seq[index] += len(self)
