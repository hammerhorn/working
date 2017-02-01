#!/bin/bash
# Depends: bashsimplecurses

#import library, please check path
#source /usr/lib/simple_curses.sh
source /usr/local/lib/simple_curses.sh

#Then, you must create a "main" function:
main (){
    #your code here, you can add some windows, text...
    rows=$(echo "`tput lines` - 5"|bc)
    window "Fibonacci sequence" "red" 31
    append_command "java -jar fibo.jar 1 $rows"
    endwin
}
#str = "$1"
#str2 "$@"

#then, you can execute loop:
main_loop .1


