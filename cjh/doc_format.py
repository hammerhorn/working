#!/usr/bin/env python
#coding=utf8
"""
docSTRING
"""
import textwrap

from ranges import gen_range
from things import Thing
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Paragraph(Thing):
    """
    A paragraph of text
    """
    ## CLASS VARIABLES ##
    invisibles = False
    no_indent = False
    Terminal()

    ## METHODS ##
    def __init__(
            self,
            text_str,
            width=int(round(Terminal.width() * .9)),
            no_indent=False):
        self.__class__.no_indent = no_indent
        super(Paragraph, self).__init__()
        self.width = width
        self.buffer = textwrap.dedent(text_str).strip()
        self.set_lmargin()

    def __lt__(self, integer):
        self.width -= integer
        if self.width < integer:
            self.width = integer
        return self

    def __gt__(self, integer):
        self >> integer
        self.width -= integer
        if self.width <= integer:
            self.width = integer
        return self

    def __rshift__(self, integer):
        self.lmargin += integer
        if self.lmargin < 0:
            self.lmargin = 0
        return self

    def __lshift__(self, integer):
        self.lmargin -= integer
        if self.lmargin < 0:
            self.lmargin = 0
        return self
            
    def __add__(self, other):
        return Section(p_list=[self, other])

    def __str__(self):
        lines2 = self.word_wrap_list
        pstr_list = ['\n']
        char = '¶' if self.__class__.invisibles is True else ' '
        pstr_list.extend((char, ' ' * (self.lmargin - 1), lines2[0], '\n'))
        pstr = ''.join(pstr_list)
        appndx_lst = []
        for index in gen_range(1, len(lines2)):
            appndx_lst.extend((' ' * self.lmargin, lines2[index], '\n'))
        str_list = [pstr]
        str_list.extend(appndx_lst)
        return ''.join(str_list)

    def __mul__(self, multi):
        plist = []
        for _ in gen_range(multi):
            plist.append(self)
        return Section(p_list=plist)

    def __getitem__(self, index):
        '''
        list() or [] will give you a list of sentences
        '''
        buf_lst = []
        for line in self.naive_wrap:
            buf_lst.append(line)
        buf = ''.join(buf_lst)
        sentences = buf.split('.')
        sentences = [sentence.lstrip('_ ') + '.' for sentence in sentences]
        return sentences[index]

    def __len__(self):
        ''' number of sentences '''
        tmp = []
        count = 0
        while True:
            try:
                count += 1
                tmp.append(self.__getitem__(count))
            except IndexError:
                break
        return len(tmp)

    def set_lmargin(self, fill=4):
        """set left margin"""
        self.lmargin = fill


        
    def cat(self, para2):
        """concatenate paragraphs?"""
        tmp_lst1, tmp_lst2 = [], []
        noindent = True

        for line in self.naive_wrap:
            tmp_lst1.append(line)
        tmp_str1 = ''.join(tmp_lst1)

        if len(tmp_str1) > 0 and tmp_str1[0] == '_':
            noindent = False
            tmp_str1 = tmp_str1.lstrip('_')

        for line in para2.naive_wrap:
            tmp_lst2.append(line)
        tmp_str2 = ''.join(tmp_lst2).lstrip('_')
        return Paragraph(\
            ''.join((tmp_str1.rstrip(), '  ', tmp_str2)), no_indent=noindent)

    @property
    def wordcount(self):
        """number of words"""
        return len(self.buffer.split())

    @property
    def naive_wrap(self):
        """
        Wrap text w/o regard to word boundaries.
        Returns a list of lines.
        """
        buf = self.buffer
        lines = []
        line_cnt = len(buf) // self.width + 1
        for _ in gen_range(line_cnt):
            if len(buf) >= self.width:
                lines.append(buf[0:self.width - 1])
                buf = buf[self.width - 1:]
            else: lines.append(buf)
        for index, line in enumerate(lines):
            if index != 0 and line[0] == ' ':
                lines[index] = lines[index].lstrip()
        return lines

    @property
    def word_wrap_list(self):
        """
        use textwrap module to wrap text
        Returns a list of lines.
        """
        buf = self.buffer.lstrip()
        i = '' if self.__class__.no_indent is True else ' ' * 5
        return textwrap.fill(\
            buf, width=self.width, initial_indent=i).split('\n')

    def justify(self):
        buf_list = []
        for line in self.word_wrap_list[:-1]:  # self.buffer.split('\n'):
            line = line.strip()
            while len(line) < self.width:
                if len(line.replace(' ', '  ')) <= self.width:
                    line = line.replace(' ', '  ')
                if len(line.split('.')) == 2:
                    line = line.replace('.', '. ')
                #if len(line) < self.width:
                #    line = line.replace('.', '. ')
                if len(line) < self.width:
                    line = line.replace(',', ', ')
            buf_list.append(line)
        buf_list.append(self.word_wrap_list[-1].strip())
        self.buffer = '\n'.join(buf_list)
        return self

class Section(Thing):
    """
    section of an article or chapter
    """
    def __init__(self, hstr='', p_list=None):
        super(Section, self).__init__()
        self.pgraph_list = p_list if p_list is not None else []
        self.heading = "{}.".format(self.__class__.count) if len(hstr) else hstr

    def __getitem__(self, index):
        return self.pgraph_list[index]

    def __add__(self, pgraph):
        #s = Section()
        self.pgraph_list.append(pgraph)
        return self
        #self.plist = self.pgraph_list[:]
        #selfplist.append(pgraph)
        #Section.count -= 1
        #return Section(p_list=plist)

    def __str__(self):
        pstr = ""
        if len(self.pgraph_list) >= 1:
            pstr = " " * (self.pgraph_list[0].lmargin)
        else: pstr = " " * 5
        pstr += self.heading.upper() + "\n"
        pstr += "\n"
        for pgraph in self.pgraph_list:
            pstr += str(pgraph)
        pstr += "\n"
        return pstr + "\n"

#class Pager(Thing):
#    def __init__(self, text):
#        self.screen = Terminal()
#        self.lines = text.split('\n')

#    def __str__(self):
        #if len(self.lines) < self.screen.width():
#        return str(len(self.lines) % self.screen.width())
