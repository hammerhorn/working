//import java.io.PrintStream;

public class fibo
{
    public static void main(String args[])
    {
        boolean interactive = false;

        if(args.length == 0){
	    interactive = true;
 	    System.out.println("Generates a term or range of terms from the Fibonacci sequence.\n");
        }

        String [] prompts = {"nth term? (1-92)"};


        // If no arguments ar given, make it an interactive shell.
        do {
   	    MyOpts Args = new MyOpts(1, args, prompts);

            /*System.err.println("\tUsage: java fibo <start term (1-46)> (<end term (1-46)>)");System.exit(1);*/
            int k = 2;
            //int ai[] = new int[46];


            //create a dynamically allocated array of at least 2
            int range = 2;
            if(Args.length() > 1){
                if(Args.getAsDouble(0) > Args.getAsDouble(1)) range = Args.getAsInt(0);
                else range = Args.getAsInt(1);
            }
            else range = Args.getAsInt(0);

            if (range < 2) range = 2;
            else if(range > 92) range = 92;

            long ai[] = new long[range];


           // Set the first two elements to 1
           ai[0] = 1;
           ai[1] = 1;


           // Each subsequent element is equal to the sum of the two previous
           for(int i = 2; i < range; i++){
     	       ai[i] = ai[i - 2] + ai[i - 1];
           }


           // Verify 1st input
           int j = Args.getAsInt(0);

           if(j <= 0 || j > range){
 	       System.out.println("Out of Range error.  Bye :)");
	       System.exit(1);
           }


           // if there is only one arg, set k & j equal
           // otherwise k is the second argument
           // Verify the 2nd argument
           if(Args.length() == 1) k = j;
           else {
	       k = Args.getAsInt(1);

               if(k <= 0 || k > range){
 	           System.out.println("Out of Range error.  Bye :)");
	           System.exit(1);
               }
           }

           System.out.println();

           if(j <= range && j > 0 && j < k){
               for(; j <= k; j++){
	           if(j < 10) System.out.print(' ');
	           System.out.println("n" + j + "  " + TuiTeX.format(ai[j - 1]));
	       }

    	       if(j > range) j = 1;
	   }
           else if(j <= range && j > 0){
	       for(; k <= j; j--){
	           if(j < 10) System.out.print(' ');
	           System.out.println("n" + j + "  " + TuiTeX.format(ai[j - 1]));
	       }

 	       if(j < 1) j = 1;
	   }
           System.out.println();
	} while(interactive);
    }
}
