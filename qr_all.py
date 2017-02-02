#!/usr/bin/env python
#coding=utf8
"""
Tries to generate a QR code for each Python file in the directory.
Many files will be too large.
"""
# Std Lib
import glob
import os
import subprocess
import sys

# Add-ons
import qrcode

# Local imports
import easycat
from versatiledialogs.lists import ItemList
from versatiledialogs.terminal import Terminal
from cjh.misc import notebook

REMARKS = """
    - convert bytes to kilobytes
    - break larger files up into pieces"""

notebook(REMARKS)

VT = Terminal()


def main():
    """
    When the file is small enough, it makes a PNG and optimizes it using optipng
    If the file is too big, an error message is displayed.
    """
    Terminal.output('')
    if len(sys.argv[1:]) > 0:
        expr_list = sys.argv[1:]
    else:
        expr_list = ['*.py']
    file_list = []
    for expr in expr_list:
        file_list += glob.glob(expr)
    file_list.sort()

    for file_ in glob.glob('*.qr.png'):
        os.remove(file_)

    for py_fname in file_list:
        try:
            dir_tkns = py_fname.split('/')
            dirname = ''
            if len(dir_tkns) > 1:
                for tkn in dir_tkns[:-1]:
                    dirname += tkn + '/'
            f_handler = open(py_fname)
            txt_str = f_handler.read()
            img = qrcode.make(txt_str)
            img_fname = '__data__/qr/{}.qr.png'.format(py_fname.replace('.', '_'))
            img.save(img_fname)
            proc = subprocess.Popen(
                'optipng {} > /dev/null 2>&1'.format(img_fname), shell=True)
            proc.wait()

            VT.report_filesave(img_fname, fast=True)

        except qrcode.exceptions.DataOverflowError:
            easycat.write(VT.fx('bn', ' [!] '))
            VT.output('<{}> {}'.format(py_fname, VT.fx('bn', 'FAILED.')))

    Terminal.wait()
    Terminal.clear()
    easycat.less(' ' + ItemList(sorted(glob.glob('__data__/qr/{}*.png'.format(dirname)))).__str__().lstrip())

if __name__ == '__main__':
    main()
    VT.start_app()
