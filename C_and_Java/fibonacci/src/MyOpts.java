//import java.io.*;
//import java.text.*;

public class MyOpts
{
    //
    // DATA
    //////////
    String [] myArgs;

    //
    // CONSTRUCTORS
    //////////////////
    public MyOpts(){}

    ////////////////////////////
    // takes an array of args //
    ////////////////////////////
    public MyOpts( String [] argz )
    {
       myArgs = argz;
    }


    //////////////////////////////////////////////////////////////////////////
    // takes an array of args, and an exact number of args, otherwise fails //
    //////////////////////////////////////////////////////////////////////////
    public MyOpts(String[] argz, int no_of_args)
    {
        myArgs = new String[argz.length];

        for(int count = 0; count < argz.length && count < no_of_args; count++)
            myArgs[count] = argz[count];

        if (lengthMinusFlags() < no_of_args){
	    System.err.println("\n\tERROR: " + no_of_args + " argument(s) expected.");
            System.exit(1);
        }
    }


    ////////////////////////////////////////////////////
    // Prints errorMEssage if number of args is wrong //
    ////////////////////////////////////////////////////
    public MyOpts(String[] argz, int no_of_args, String errorMessage)
    {
        myArgs = new String[argz.length];
        errorMessage = "\n" + errorMessage + "\n";

        for(int count = 0; count < argz.length && count < no_of_args; count++)
            myArgs[count] = argz[count];

        if(argz.length < no_of_args){ 
            System.err.println(errorMessage);
            System.exit(1);
        } 
    }
    

    ///////////////////////////////////////////////
    // Reads from stdin if argument not present. //
    //
    // This constructpr might freak out if it encounters a flag or option.
    public MyOpts(int min_no_of_args, String[] argz)
    {
	if(argz.length >= min_no_of_args)
            myArgs = argz;
	else { 
 	    myArgs = new String[min_no_of_args];
            for(int count=0;count < argz.length; count++)
                myArgs[count] = argz[count];
            for(int count = argz.length; count < min_no_of_args; count++)
                myArgs[count] = Keyboard.readLine();                 
	}
    }


    /////////////////////////////////////////////////////////////////////
    // takes a minimum no. of args, array of args, custom error string //
    /////////////////////////////////////////////////////////////////////
    public MyOpts(int min_no_of_args, String[] argz, String errorMessage)
    {
        errorMessage = "\n" + errorMessage + "\n";
        if(argz.length >= min_no_of_args)
            myArgs=argz;
        else {
            System.err.println(errorMessage);
            System.exit(1);
        }
    }

    //////////////////////////////////
    // This constructor seems buggy //
    //////////////////////////////////
    public MyOpts(int min_no_of_args, String[] argz, String[] prompts, String errorMessage)
    {
        errorMessage = "\n" + errorMessage + "\n";
        if(argz.length >= min_no_of_args)
            myArgs=argz;
        else{ 
            myArgs = new String[min_no_of_args];
            System.err.println(errorMessage);    

            for(int count = 0; count < myArgs.length; count++)
                myArgs[count] = argz[count];
            for(int count = 0; count < argz.length; count++)
                System.out.println(prompts[count] + " = " + argz[count]);
            for(int count=argz.length;count<min_no_of_args;count++){
                System.out.print(prompts[count]);
                myArgs[count]=Keyboard.readLine();                 
            }
        }
    }
    
    public MyOpts(int min_no_of_args, String[] argz, String[] prompts)
    {
        MyOpts temp = new MyOpts(argz);
	if(temp.stripFlags().length() >= min_no_of_args)
            myArgs = argz;
	else{ 
	    myArgs = new String[min_no_of_args];

            for(int count = 0;count < argz.length; count++)
                myArgs[count]=argz[count];

	    int promptCount = 0;
            for(int count = temp.stripFlags().length(); count < min_no_of_args; count++){
	        System.out.print(prompts[promptCount]);
                myArgs[count]=Keyboard.readLine();
                promptCount++;                 
            }
        }
    }

/*    ///////////////////////////////////////////////////////////////////////////////////////
    // takes a minimum no. of args, array of args, array of prompts, custom error string //
    ///////////////////////////////////////////////////////////////////////////////////////
    public MyOpts(int min_no_of_args, String[] argz, String[] prompts, String errorMessage, boolean interactive)
    {
     //  errorMessage="\n"+errorMessage+"\n";
       if(argz.length>=min_no_of_args){ myArgs=argz;}
       //else
       //{ 
         // myArgs = new String[min_no_of_args];
          //System.err.println(errorMessage);    
          //for(int count=0;count < argz.length; count++)
          //{
           //   myArgs[count]=argz[count];
         // }
    
	   //           System.err.println("("+min_no_of_args+" or more arguments expected.)");
      if(interactive)
      {
          System.out.println("Going into interactive mode");
myArgs=stripFlags().getStringArray();
          for(int count=argz.length;count<min_no_of_args;count++)
          {
             System.out.print(prompts[count]+"?");
             myArgs[count]=Keyboard.readLine();                 
          }
      }
   }
       // System.out.println();
*/



    //
    // GET & SET
    ///////////////
    public int length()
    {
        return myArgs.length;
    } 


    public int lengthMinusFlags()
    {
	int net_length = this.length();
	for(int x = 0; x < this.length(); x++)
	    if(this.myArgs[x].charAt(0) == '-') 
		   net_length--;
        return net_length;
    }


    public int countFlags()
    {	
        int flagCount = 0;
        for(int x = 0; x < this.length() - 1; x++)
 	    if(this.myArgs[x].charAt(0) == '-')
	        for(int q = 0; q < myArgs[x].length() - 1; q++)
	 	    flagCount++;
       return flagCount;
    }


    public String getElement(int subscript)
    { 
        if(subscript > myArgs.length-1){
	    System.err.println("Expecting argument(s) of type: String");
            System.exit(1);
        }
	return myArgs[subscript];
    }


    public double getAsDouble(int subscript)
    { 
        if(subscript > this.length() - 1){
	    System.err.println("Expecting argument(s) of type: double");
            System.exit(1);
	}
	return Double.parseDouble(this.getElement(subscript));
    }


    public int getAsInt(int subscript)
    { 
        if(subscript > length() - 1){
	   System.err.println("Expecting argument(s) of type: int");
           System.exit(1);
	}
	return Integer.parseInt(getElement(subscript));
    }

    
    public MyOpts stripFlags()
    {
        String[] stript = new String [this.lengthMinusFlags()];

	int striptCount = 0;
        for(int rawCount = 0; rawCount < this.length(); rawCount++)
            if(getElement(rawCount).charAt(0) != '-'){
	        stript[striptCount] = getElement(rawCount); 
		striptCount++;
	    }
	    
	    /*	for(int rawCount=0; rawCount < stript.length; rawCount++)
        {
	    if(myArgs[rawCount].charAt(0)!='-') 
            {
	        stript[striptCount]=this.myArgs[rawCount];
		    System.out.println("stript["+striptCount+"]=myArgs["+rawCount+"];");
		striptCount++;
	    }
*///	    System.out.println(striptCount+", "+rawCount);
	    //System.out.print();
	    //System.out.print();
	//for(int p=0;p<stript.length;p++){/*System.out.print(stript[p]+" ");*/}
        
	MyOpts i = new MyOpts(stript);
	return i;
    }

    
    public static boolean detectShortOption(String [] Args,char c)
    {
        boolean flagDetected = false;
        for(int count = 0; count < Args.length; count++)
            if(Args[count].charAt(0) == '-')
                for(int j = 1; j < Args[count].length(); j++)
	 	    if(Args[count].charAt(j) == c) flagDetected = true;
        return flagDetected;
    }

    
    public boolean detectShortOption(char c)
    {
	boolean flagDetected = false;
        for(int count = 0; count < myArgs.length; count++)
            if(this.myArgs[count].charAt(0) == '-')
               for(int j = 1; j < myArgs[count].length(); j++)
		   if(myArgs[count].charAt(j) == c)
                       flagDetected = true;
	return flagDetected;
    }

    public int firstFlagIndex()
    {
	for(int count = 0; count < myArgs.length; count++)
            if(myArgs[count].charAt(0) == '-')
                return count;
        return -1;
    }

    public String getShortOptions()
    {      
	String flags = "";
	for(int count = 0; count < length(); count++)
            if(myArgs[count].charAt(0) == '-')
 	        if(myArgs[count].length() >= 2)
                    for(int j = 1; j < myArgs[count].length(); j++)
		        flags += myArgs[count].charAt(j);
        return flags;
    }

    public void setStringArray(String [] a)
    {
        myArgs = a;
    }

    public String [] getStringArray()
    {
        return myArgs;
    }


    //
    // I/O
    /////////
    public void printArgs()
    {
        System.out.print("{");
	for(int count = 0; count < this.length(); count++){
	    System.out.print(myArgs[count]);
            if(count != this.length() - 1)
                System.out.print(", ");
	}
	System.out.println("}");
	System.out.println();
    }
}
