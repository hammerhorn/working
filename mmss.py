#!/usr/bin/env python
"""
    Usage: ./mmss.py mins:secs --> seconds
    Usage: ./mmss.py hrs:mins  --> minutes
    Usage: ./mmss.py seconds   --> mins:secs
    Usage: ./mmss.py minutes   --> hrs:mins
"""
import sys


def main():
    """main function"""
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(__doc__)  # pylint: disable=C0325
        elif ':' in sys.argv[1]:
            mmss = tuple(sys.argv[1].split(':'))
            try:
                mins = int(mmss[0])
            except ValueError:
                mins = 0
            try:
                secs = float(mmss[1])
            except ValueError:
                secs = 0.0
            total_seconds = mins * 60.0 + secs
            print(total_seconds)  # pylint: disable=C0325

        else:
            total_seconds = float(sys.argv[1])
            mins = int(total_seconds) // 60
            secs = total_seconds % 60
            print('{:d}:{:02g}'.format(mins, secs))  # pylint: disable=C0325

    except IndexError:
        print('Argument required.')  # pylint: disable=C0325

    except ValueError:
        print('Invalid argument.')  # pylint: disable=C0325
        print(__doc__)  # pylint: disable=C0325

if __name__ == '__main__':
    main()
