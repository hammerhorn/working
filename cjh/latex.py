#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import os
import sys

from cjh.doc_format import Paragraph, Section
from ranges import gen_range
from things import Thing
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class LatexObj(Thing):
    """
    class for dealing with LaTeX files
    """
    def import_file(self, filename):
        """
        read-in the file, initializing the object
        """
        def read_file_lines():
            """
            Read in lines from file.
            """

            def file_error():
                """
                If no regular file exists, print an error message and exit.
                """
                current_dir = os.getcwd()
                if filename in ('.', '..', '/') or filename in os.listdir(
                        current_dir):
                    error = '{}: {}: Is a directory'
                else:
                    error = '{}: {}: No such file or directory'
                    sys.exit(error.format(sys.argv[0], filename))

            try:
                fhandler = open(filename)
                self.lines = fhandler.readlines()
                fhandler.close()
            except IOError:
                file_error()

        def strip_whitespace():
            """
            Get rid of whitespace on the left and right.
            """
            for line in self.lines:
                self.lines[self.lines.index(line)] = line.strip()

        def strip_comments():
            """
            Remove comments, i.e., lines starting with '%'
            """
            line_count = len(self.lines)
            lines_to_delete = []

            for indx in gen_range(line_count):
                if len(self.lines[indx]) > 0 and self.lines[indx][0] == '%':
                    lines_to_delete.append(indx)
            for i in lines_to_delete:
                del self.lines[i]
                for line_index in gen_range(1, len(lines_to_delete)):
                    lines_to_delete[line_index] -= 1

        read_file_lines()
        strip_whitespace()
        strip_comments()

    def __init__(self, file_, margin=10):

        def _initialize_fields():
            """
            assign a default value to fields
            """
            self.margin = margin
            self.width = Terminal.width() - margin * 2
            self.tabpoints = margin, self.width
            self.author = None
            self.title = None
            self.date = ''
            self.buffer = ''
            self.lines = []
            self.pgraph_no = 0
            self.section_no = 0
            self.p_list = []
            self.s_list = []

        super(LatexObj, self).__init__()
        _initialize_fields()
        self.import_file(file_)
        self.scan_lines()

    def make_title(self):
        """
        Print a nice title page.
        """
        if self.title is not None:
            out_str_list = []
            out_str_list.extend(('\n' * (Terminal.height() // 2 - 2),
                                 ' ' * 4 + Terminal.fx('bu', (
                                     self.title)).center(Terminal.width())))
            if self.author is not None:
                out_str_list.append(
                    '\n\n{}\n\n{}'.format('by'.center(
                        Terminal.width()), self.author.center(Terminal.width())))
            out_str_list.extend(('\n' * (Terminal.height() // 2 - 2), '-' * Terminal.width()))
            if self.section_no == 0:
                out_str_list.append('\n' * 4)
            return ''.join(out_str_list)
        else:
            return '[No title]'

    def print_toc(self):
        """
        Create a table of contents and print to the screen.
        """
        out_str_list = []
        any_visible = False
        for section_index in gen_range(len(self.s_list)):
            if self.s_list[section_index].heading not in (None, '', '0') and\
               self.s_list[section_index].heading[0].isdigit():
                any_visible = True
        if any_visible is True:
            out_str_list.append('CONTENTS'.center(Terminal.width()))

            for section in self.s_list:
                if self.s_list[section_index].heading not in (None, '', '0')\
                   and self.s_list[section_index].heading[0].isdigit():
                    out_str_list.append(
                        section.heading.center(Terminal.width()))
                out_str_list.append('\n')
            out_str_list.extend(
                (('-' * (Terminal.width() // 2)).center(
                    Terminal.width()), '\n\n') * 2)
        return ''.join(out_str_list)

    def print_sections(self):
        """
        Print out all sections
        """
        out_str_list = []

        #top margin == left margin / 3
        out_str_list.append('\n' * int(self.tabpoints[0]/3.0))
        if len(self.s_list) >= 1 and len(self.s_list[0].pgraph_list) > 0:
            out_str_list.append(str(self.s_list[0]))
        for section_index in gen_range(1, len(self.s_list)):
            out_str_list.append(str(self.s_list[section_index]))
        return ''.join(out_str_list)

    def __str__(self):
        return ''.join(
            (self.make_title(), self.print_toc(), self.print_sections()))

    def store_paragraph(self, no_indent):
        """
        Use contents of 'buffer' to construct a new Paragraph object,
        and we clear 'buffer' to read in the next paragraph of text.
        """
	#print "begin store_paragraph()"
        self.pgraph_no += 1
        if len(self.buffer) > 0:
            self.buffer = self.easy_subs(self.buffer)

            #self.strip_unknown_tags()

            paragraph = Paragraph(self.buffer, self.tabpoints[1], no_indent)
            paragraph.set_lmargin(self.tabpoints[0])
            #print "add to section"
            self.s_list[len(self.s_list) - 1] += paragraph
            self.buffer = ''
	#print "end store_paragraph()"

    def easy_subs(self, buffer):
        """
        reimplement using a dictionary
        """
        tmp = buffer
        buffer = buffer.replace('\\\\', '\n')
        buffer = buffer.replace(r'\dots', '(...)')
        buffer = buffer.replace("\\'a", 'á')
        buffer = buffer.replace("\\'i", 'í')
        buffer = buffer.replace('---', '—')
        buffer = buffer.replace('--', '–')
        buffer = buffer.replace("``", '“')
        buffer = buffer.replace("''", '”')
        buffer = buffer.replace("'", '’')
        buffer = buffer.replace('`', '‘')
        buffer = buffer.replace('\\^C', 'Ĉ')
        buffer = buffer.replace('\\^c', 'ĉ')
        buffer = buffer.replace('\\^G', 'Ĝ')
        buffer = buffer.replace('\\^g', 'ĝ')
        buffer = buffer.replace('\\^H', 'Ĥ')
        buffer = buffer.replace('\\^h', 'ĥ')
        buffer = buffer.replace('\\^J', 'Ĵ')
        buffer = buffer.replace('\\^j', 'ĵ')
        buffer = buffer.replace('\\^S', 'Ŝ')
        buffer = buffer.replace('\\^s', 'ŝ')
        buffer = buffer.replace('\\u{u}', 'ŭ')
        buffer = buffer.replace('\\LaTeX{', 'LaTeX')
        #print '{} = easy_subs({})'.format(buffer, tmp)
        return buffer

    def strip_unknown_tags(self):
        """
        If an unknown tag is detected in 'buffer', attempt to remove it
        gracefully.
        """
        while(self.buffer.find('\\') >= 0) and\
             self.buffer[self.buffer.find('\\') + 2] != '\n':
            if (self.buffer.find('section') == self.buffer.find('\\') + 1) or \
                (self.buffer.find('title') == self.buffer.find('\\') + 1) or \
                len(self.buffer[
                        self.buffer.find('\\'):self.buffer.find('}') + 1]) == 0:
                break
            self.buffer = self.buffer[:self.buffer.find('\\')] +\
                self.buffer[self.buffer.find('}') + 2:]

    def open_new_section(self, headline=''):
        """
        Create a new section, and reset 'pgraph_no'
        """
        self.pgraph_no = 0
        self.s_list.append(Section(headline))

    def parse_section_tag(self, line):
        """
        Append a new empty Section, and process heading number.
        """
        #print "begin parse_section_tag()"
        if line.find(r'\section{') >= 0:
            self.section_no += 1
            self.open_new_section(str(self.section_no) + '. ' + line[(line.find(
                r'\section{') + 9):(line.find('}'))])
        elif line.find(r'\section*{') >= 0:
            self.open_new_section(line[(line.find(r'\section*{') + 10):(
                line.find('}'))])
        else: sys.exit('Error in string ' + r'\section')
        line = line[(line.find('}') + 1):]

    def scan_lines(self):
        """
        Scan each line in 'lines'
        """
        #print "begin scan_lines()"
        for line in self.lines:
           #print 'begin loop: "{}"'.format(line)

	   #if line not empty
            if line not in ('', '\n'):
               #get title
                if line.find('\\title') >= 0:
                    # Modify to allow nested {}s
                    self.title = self.easy_subs(
                        line[(line.find('{') + 1):(line.find('}'))])
                    #self.title = self.title.strip()
                elif line.find('\\author') >= 0:
                    self.author = line[(line.find('{') + 1):(line.find('}'))]

               # If '\section' tag is detected, create a new section and add an
#entry to the table of contents.
                elif line.find(r'\section') >= 0:
                    self.parse_section_tag(line)

                elif line.find(r'\hrule') >= 0:
                    self.buffer = '-' * Terminal.width()
                    self.store_paragraph(True)

               # If the current line is  not empty, append it to the buffer.
                else:
                    if len(self.s_list) == 0 and len(line) != 0:
                        Section.count = -1
                        self.open_new_section() # Introduction")
		       #print "section=0"

                    self.buffer = ''.join((self.buffer, line, ' '))

           # If it's a blank line, we store the Paragraph and prepare to read in
#a  new one.
           #    strip_unknown_tags()
            else:
                self.store_paragraph(False)



##def process_text():
##    global lines
##    global section_no
##    global line_no
##    global screen
##    if lines[line_no].find('\textbf{') >= 0:
##        section_no += 1
##        screen.bold_write(lines[line_no][(lines[line_no].find('\{') + 8):(
#lines[line_no].find('}'))])
##    elif lines[line_no].find('\section*{') >= 0:
##        open_new_section(lines[line_no][(lines[line_no].find('\section*{') +
#10):(lines[line_no].find('}'))])
##    else:
##        sys.exit("Error in string " + "\section")
##    lines[line_no] = lines[line_no][(lines[line_no].find("}") + 1):]
