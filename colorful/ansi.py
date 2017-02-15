import re

class Ansi(object):
    ctrl_char = '\033[%sm'

    BLACK = ctrl_char % '38;5;0'
    WHITE = ctrl_char % '38;5;231'
    ON_CYAN = ctrl_char % '48;5;6'
    ON_GREY = ctrl_char % '48;5;7'
    UNDERLINE = ctrl_char % '4'
    BOLD = ctrl_char % '1'
    REVERSE = ctrl_char % '7'
    RESET = ctrl_char % '0'

    @staticmethod
    def strip_ansi(in_str):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', in_str)
