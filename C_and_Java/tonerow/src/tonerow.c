#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

void swap(int*, int*);
void printArray(int[], int);
void randomize(int[], int);

int main (int argc, char **argv)
{
    // Get Args //
    char *nvalue = NULL;
    int index, c, nint=0;
    opterr = 0; // error verbosity off

    while ((c = getopt (argc, argv, "n:")) != -1)
        switch (c)
        {
          case 'n':
	    nvalue = optarg;
            nint = atoi(nvalue);
	    break;
          case '?':
	    if(optopt == 'n')
	        fprintf(stderr, "Option -%c requires an argument.\n", optopt);
	    else if (isprint (optopt))
	        fprintf(stderr, "Unknown option `-%c'.\n", optopt);
	    else
	        fprintf(stderr, "Unknown option character `\\x%x'.\n", optopt);
	    return 1;
          default:    // Not sure if this
	    abort (); // code is reachable...
        }

    for(index = optind; index < argc; index++)
        printf ("Non-option argument %s\n", argv[index]);

    if(nint == 0)
        nint = 12;
  
    // Create sequence 1 thru n.
    int arr[nint],
        count;
    for(count = 0; count < nint; count++)
        arr[count] = count; // + 1

    // Shuffle, and print  
    randomize(arr, nint);
    printArray(arr, nint);
  
    return 0;
}

// A utility function to print an array
void printArray (int arr[], int n)
{
    int i;
    for(i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// A function to generate a random permutation of arr[]
void randomize ( int arr[], int n )
{
    // Use a different seed value so that we don't get same
    // result each time we run this program
    srand(time(NULL));

    // Start from the last element and swap one by one. We don't
    // need to run for the first element that's why i > 0
    int i;
    for(i = n - 1; i > 0; i--){

        // Pick a random index from 0 to i
        int j = rand() % (i + 1);

        // Swap arr[i] with the element at random index
        swap(&arr[i], &arr[j]);
    }
}

// A utility function to swap to integers         
void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
