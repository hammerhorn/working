import re

class Ansi(object):
    BLACK = '\033[38;5;0m'
    WHITE = '\033[38;5;231m'

    ON_CYAN = '\033[48;5;6m'
    ON_GREY = '\033[48;5;7m'

    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'

    @staticmethod
    def strip_ansi(in_str):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', in_str)
        
