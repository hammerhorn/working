#!/usr/bin/env python3
"""
    Usage: ./mmss.py mins:secs --> seconds
    Usage: ./mmss.py hrs:mins  --> minutes
    Usage: ./mmss.py seconds   --> mins:secs
    Usage: ./mmss.py minutes   --> hrs:mins
"""
import sys
from cjh import misc

        
def main():
    """
    main function
    """
    misc.catch_help_flag(help_str=__doc__.rstrip())
    print(misc.mmss_convert(sys.argv[1]))


if __name__ == '__main__':
    main()
