#include <math.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <time.h>

void print_title(void);
void sigintHandler(int);  // If ^C is pressed, unhide the cursor. 

int main(int argc, char* argv[]) 
{
    unsigned int toggle = 0, // isn't there anyway to economize this?
                 iter_count = 0,
                 width,
                 indent,
                 count;

    double s;
    struct winsize ws;

    signal(SIGINT, sigintHandler);
    ioctl(0, TIOCGWINSZ, &ws);
    print_title();
    printf("\033[?25l"); // Hide cursor

    while(1){
        s = iter_count / 4.0;
        indent = ((ws.ws_col - 10) * sin(s) + ws.ws_col - 8) / 2;
        for(count = 0; count < indent; count++)
            printf(" ");
        if(toggle == 1) {
            printf("CREATIVE\n");
            toggle = 0;
        }
        else {
            printf("COMPUTING\n");
            toggle = 1;
        }

        nanosleep((struct timespec[]) { {
	    0, 25000000}}, NULL);

        iter_count++;
    }
    return 0;
}

void print_title(void)
{
    int count;
    printf("\x1b[2J\x1b[H");
    for(count = 0; count < 30; count++) printf(" ");
    printf("SINE WAVE\n");
    for(count = 0; count < 15; count++) printf(" ");
    printf("CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY");
    for(count = 0; count < 5; count++) printf("\n");
    printf("Press <ENTER> to begin...");
    while( getchar() != '\n');
}

void sigintHandler (int sig_num)
{
    signal(SIGINT, sigintHandler);
    printf("\033[?25h");
    exit(0);
}
