#!/bin/sh
gcc -o tonerow -O3 src/tonerow.c
strip -s tonerow
chmod +x tonerow
