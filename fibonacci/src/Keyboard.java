//package MyIO;

import java.io.*;

public class Keyboard
{

    private static BufferedReader reader;

    public Keyboard()
    {
    }

    public static String raw_input(String prompt)
    {
	System.out.print(prompt);
        return Keyboard.readLine();
    }

    public static String readLine()
    {
        String s = "";
        try
	    {
		s = reader.readLine();
	    }
        catch(IOException ioexception)
	    {
		System.out.println("Error in Keyboard class:" + ioexception);
		quit();
	    }
        return s;
    }

    public static int readInt()
    {
        int i = 0;
        try
	    {
		i = Integer.parseInt(readLine().trim());
	    }
        catch(NumberFormatException numberformatexception)
	    {
			System.out.println("Error in Keyboard.readInt()\n" + numberformatexception);
		quit();
	    }
        return i;
    }

    public static double readDouble()
    {
        double d = 0.0D;
        try
	    {
		d = Double.parseDouble(readLine().trim());
	    }
        catch(NumberFormatException numberformatexception)
	    {
		System.out.println("Error in Keyboard.readDouble()\n" + numberformatexception);
		quit();
	    }
        return d;
    }

    public static double readDouble(String prompt){
	System.out.print(prompt);
        return Keyboard.readDouble();
    }


    private static void quit()
    {
	        System.out.println("\nTerminating the program.");
        System.exit(1);
    }

    static 
    {
        reader = new BufferedReader(new InputStreamReader(System.in));
    }
}
