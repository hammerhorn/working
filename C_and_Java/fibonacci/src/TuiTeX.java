import java.text.DecimalFormat;
import java.util.*;
import java.math.BigDecimal;

public class TuiTeX
{
    static final int LeftOfCenter = 6;
	
    public TuiTeX(){}

    //Alternately, printf("%d") can be used to right justify things

    ///////////////////////////////////////////////////
    // Right-align a double in a 6-space-wide column //
    ///////////////////////////////////////////////////

    public static String rightAlign(String s, int i)
    {
	while(i > s.length()) s = ' ' + s;
        return s;

        ////////////////////////////////////////////////////////
        // This is the Java way, but I must be doing it wrong //
	////////////////////////////////////////////////////////

	//Formatter fmt = new Formatter();
	//fmt.format("%" + i + "s", s);
        //return fmt.toString();
    }

    public static String rightAlign(double d)
    {
        DecimalFormat decimalformat1 = new DecimalFormat("0.#E0");
        DecimalFormat decimalformat2 = new DecimalFormat("##0.###");
        Double double1 = new Double(d);
        DecimalFormat decimalformat;

        if(("" + (int)double1.doubleValue()).length() <= 5 && 
          double1.doubleValue() >= 0.10000000000000001D || 
          double1.doubleValue() <= 0.0D){
            decimalformat = decimalformat2; 
        } 
 
        else decimalformat = decimalformat1;
        return String.format("%1$" + 6 + "s",decimalformat.format(d));    
    }


    ////////////////////////////////////////////////////
    // Right-align a double in an n-space-wide column //
    ////////////////////////////////////////////////////
    public static String rightAlign(double d, int i)
    {
        DecimalFormat decimalformat1 = new DecimalFormat("0.#E0");
        DecimalFormat decimalformat2 = new DecimalFormat("##0.###");
        Double double1 = new Double(d);
        DecimalFormat decimalformat;

        if(("" + (int)double1.doubleValue()).length() <= 5 && 
          double1.doubleValue() >= 0.10000000000000001D || 
          double1.doubleValue() <= 0.0D) {
            decimalformat = decimalformat2;
        }
 
        else decimalformat = decimalformat1;
        return String.format("%1$" + i + "s",decimalformat.format(d));    
    }

 
    //////////////////////////////////////////////////////////////////////////
    // Format a double into either scientific notation or a 3-place decimal //
    //////////////////////////////////////////////////////////////////////////
    public static String format(double d)
    {
        DecimalFormat decimalformat1 = new DecimalFormat("0.###E0");
        DecimalFormat decimalformat2 = new DecimalFormat(",##0.###");
        Double double1 = new Double(d);
        DecimalFormat decimalformat;

        if(("" + (int)double1.doubleValue()).length() <= 7 && 
          double1.doubleValue() >= 0.10000000000000001D || 
          double1.doubleValue() <= 0.0D) {
            decimalformat = decimalformat2;
        }

        else decimalformat = decimalformat1;
        return decimalformat.format(d);
        // 5.7 ⨉ 10^4
    }


    //////////////////////////////////////////////////////////////////////////
    // Format a double into either scientific notation or a 3-place decimal //
    //////////////////////////////////////////////////////////////////////////
    public static String money(double d)
    {
	BigDecimal a = new BigDecimal(d);
        BigDecimal floored = a.setScale(2, BigDecimal.ROUND_DOWN);

	/* DecimalFormat decimalformat = new DecimalFormat(",##0.00");
	   decimalformat.setRoundingMode();*/

	return "$" + floored; //.doubleValue();
    }

    ///////////////////////////////////////////////////////////
    // Format an int, using scientific notation if necessary //
    ///////////////////////////////////////////////////////////
    public static String format(int i)
    {
        DecimalFormat decimalformat = new DecimalFormat("###,##0");
        return decimalformat.format(i);
    }

    public static String format(long i)
    {
        DecimalFormat decimalformat = new DecimalFormat("###,##0");
        return decimalformat.format(i);
    }


    //////////////////
    // Skip 2 lines //
    //////////////////
    public static void vspace()
    {
        System.out.println("\n");
    }

 
    ////////////////////////////////////
    // Skip a certain number of lines //
    ////////////////////////////////////
    public static void vspace(int i)
    {
        for(int j = 0; j < i; j++){
	    System.out.println();
        }
    }

    public static void hfill(int i)
    {
	for (int j = 0; j < i; j++) System.out.print(' ');
    }


    //////////////////////////////////////////////////
    // Make a horizontal line by made of 80 hyphens //
    //////////////////////////////////////////////////
    public static void hrule()
    {
	for(int count = 0; count < 80; count++) System.out.print('-');
        System.out.println();
    }

    public static void hrule(int i)
    {
	for(int count = 0; count < i; count++)System.out.print('-');
        System.out.println();
    }

    public static void HRULE()
    {
	for(int count = 0; count < 80; count++){
	    System.out.print('=');
        }
        System.out.println();
    }

    public static void hrule(char c)
    {
	for(int count=0;count<80;count++){
	    System.out.print(c);
        }
        System.out.println();
    }

    
    ////////////////////////////////////////////////////////////
    // Print a one-line string centered, with a border of *'s //
    ////////////////////////////////////////////////////////////
    public static String box(String s)
    {
	int bannerWidth = s.length() + 4, 
            columnTotal = 80,
            i;

        double emptyColumns = columnTotal - bannerWidth,
               emptyColumnsOver2 = emptyColumns / 2D;

        String content = "\n";

        i = (int)emptyColumnsOver2 - 6;

        for(int j = 0; j < i; j++) content += ' ';

        for(int k = 0; k < bannerWidth; k++) content+='*';

        content+='\n';

        for(int l = 0; l < i; l++) content+=' ';

        content+="* " + s + " *\n";

        for(int i1 = 0; i1 < i; i1++) content += ' ';

        for(int j1 = 0; j1 < bannerWidth; j1++) content+='*';

	content+="\n";

	return content;
    }

    
    ///////////////////////////////////////////////////////////////
    // Print a one-line string a specified number of spaces from //
    // the left edge, with a border of *'s                       //
    ///////////////////////////////////////////////////////////////
    public static String box(String s, int fromLeft)
    {	
        int bannerWidth = s.length() + 4;
	//                columnTotal = 80;
	String content="\n";

        int j = fromLeft;

        bannerWidth = s.length() + 4;

        for(int k = 0; k < j; k++) content+=' ';

        for(int l = 0; l < bannerWidth; l++)
	{
	   content+='*';
	}

	content+='\n';

        for(int i1 = 0; i1 < j; i1++)
	{
	   content+=' ';
	}

        content+="* " + s + " *\n";

        for(int j1 = 0; j1 < j; j1++)
	{
	   content+=' ';
	}

        for(int k1 = 0; k1 < bannerWidth; k1++)
	{
	   content+='*';
	}

	return content + '\n';
    }


    ////////////////////////////////////////////////////////////////////////
    // Print a one-line string indented a specified number of spaces from //
    // the center point edge, with a border of *'s                        //
    ////////////////////////////////////////////////////////////////////////
    public static String box(int i, String s)
    {
        int columnTotal = 80,
        bannerWidth = s.length() + 4;
        double d = columnTotal - bannerWidth;
        double d1 = d / 2D;
        int j;
	String content="\n";

        if(d / 2D != 0.0D) j = (int)d1 - (i * -1 + 1);
        j = (int)d1 - i * -1;

        for(int k = 0; k < j; k++) content += ' ';

        for(int l = 0; l < bannerWidth; l++) content += '*';

        content += '\n';

        for(int i1 = 0; i1 < j; i1++) content += ' ';

        content += "* " + s + " *\n";

        for(int j1 = 0; j1 < j; j1++) content += ' ';

        for(int k1 = 0; k1 < bannerWidth; k1++) content += '*';

	content += "\n";
	return content;
    }


    ////////////////////////////////////////////////////////////
    // Print a one-line string centered, with a custom symbol //
    ////////////////////////////////////////////////////////////
    public static String box(char c, String s)
    {
        int columnTotal = 80;
        int bannerWidth = s.length() + 4;
        double d = columnTotal - bannerWidth;
        double d1 = d / 2D;
        int i;
	String content = "\n";
        if(d / 2D != 0.0D) i = (int)d1 - 7;
        i = (int)d1 - 6;

        for(int j = 0; j < i; j++) content += ' ';

        for(int k = 0; k < bannerWidth; k++) content += c;

	content += '\n';
        for(int l = 0; l < i; l++) content += ' ';

        content += c + " " + s + " " + c + "\n";
        for(int i1 = 0; i1 < i; i1++) content += ' ';

        for(int j1 = 0; j1 < bannerWidth; j1++) content += c;

	content += "\n";
	return content;
    }


    //////////////////////////////////////////////////////////////////////////////////
    // Print a one-line string indented from the center point, with a custom symbol //
    //////////////////////////////////////////////////////////////////////////////////
    public static String box(char c, int i, String s)
    {
        int columnTotal = 80;
        int bannerWidth = s.length() + 4;
        double d = columnTotal - bannerWidth;
        double d1 = d / 2D;
        int j;
	String content="\n";

        if(d / 2D != 0.0D) j = (int)d1 - (i * -1 + 1);
        j = (int)d1 - i * -1;
	//content+="\n";
        for(int k = 0; k < j; k++) content+=' ';
        for(int l = 0; l < bannerWidth; l++) content+=c;
	content += '\n';
        for(int i1 = 0; i1 < j; i1++) content += ' ';
        content += c + " " + s + " " + c + "\n";
        for(int j1 = 0; j1 < j; j1++) content += ' ';
        for(int k1 = 0; k1 < bannerWidth; k1++) content+=c;
	content += "\n";
	return content;
    }


    ///////////////////////////////////////////////////////////////////////////////
    // Print a one-line string indented from the left edge, with a custom symbol //
    ///////////////////////////////////////////////////////////////////////////////
    public static String box(char c, String s, int i)
    {
	String str = "\n";
        //int columnTotal = 80;
        int j = i;
	//        str+="\n\n\n";
        int bannerWidth = s.length() + 4;
        for(int k = 0; k < j; k++) str += ' ';
        for(int l = 0; l < bannerWidth; l++) str += c;
	str += '\n';
	for(int i1 = 0; i1 < j; i1++) str += ' ';
        str += c + " " + s + " " + c + "\n";
        for(int j1 = 0; j1 < j; j1++) str += ' ';
	for(int k1 = 0; k1 < bannerWidth; k1++) str += c;
        str += "\n";
	return str;
    }

    public static void underline(String s)
    {
	System.out.println(' ' + s);
	for(int x = -2; x < s.length(); x++) System.out.print('-');
	System.out.println();
    }

    public static void underline(String s, int indent)
    {
	for(int x = 0; x < indent; x++) System.out.print(" ");
	System.out.println(' ' + s);
	for(int x = 0; x < indent; x++) System.out.print(" ");
	for(int x = -2; x < s.length(); x++) System.out.print('-');
	System.out.println();

    }
    
    public static void ul(String s, char c)
    {
	System.out.println(' ' + s);
	for(int x = -2; x < s.length(); x++) System.out.print(c);
	System.out.println();
    }

    
    public static void ul(String s, int indent, char c)
    {
	for(int x = 1; x < indent; x++) System.out.print(" ");
	System.out.println("  " + s);
	for(int x = 0; x < indent; x++) System.out.print(" ");
	for(int x = -2; x < s.length(); x++) System.out.print(c);
	System.out.println();
    }

    public static void ul(String s)
    {
	//        System.out.print("begin");
	System.out.println("  " + s);
        System.out.print(" ");
	for(int x = -2; x < s.length(); x++) System.out.print("=");
	System.out.println();
        //System.out.print("end");
    }
    
    public static void heading(String s)
    {
        vspace(1);
        System.out.println(s);
        hrule();
    }
    

    /////////////////////////////
    // cast a double as an int //
    /////////////////////////////
    public static int trunc(double d)
    {
        return (int)d;
    }

    public static void itemize(String title, String[] list)
    {
	System.out.println();
	ul(title);
	System.out.println();
        System.out.println(" - " + list[0]);
        int tier_length = 0;
	for(int x = 1; x < list.length; x++){
            if(list[x].charAt(0) == '-'){
                //if(tier_length == 0) System.out.println();
                tier_length++;
		System.out.print("  ");
                System.out.println(" + " + list[x].substring(1, list[x].length()));
	    }
            else {
                if(tier_length != 0) System.out.println();
                System.out.println(" - " + list[x]);
                tier_length = 0;
	    }
        }
	System.out.println();
    }

    public static void itemize(String title, ArrayList<String> list)
    {
	System.out.println();
	ul(title);
	//System.out.println();
        System.out.println(" - " + list.get(0));
        int tier_length = 0;
	for(int x = 1; x < list.size(); x++){
            if(list.get(x).charAt(0) == '-'){
                //if(tier_length == 0) System.out.println();
                tier_length++;
		System.out.print("  ");
                System.out.println(" + " + list.get(x).substring(1, list.get(x).length()));
	    }
            else{
                if(tier_length != 0) System.out.println();
                System.out.println(" - " + list.get(x));
                tier_length = 0;
	    }
        }
	System.out.println();
    }

    public static String emph(String s)
    {
	return "[" + s + "]";
    }

    public static void subheading(String s)
    {
        System.out.println(" == " + s + " ==\n");
    }

    public static void enumerate(String title, String[] list)
    {
	System.out.println();
	ul(title);
	for(int x = 1; x <= list.length; x++){
	    System.out.println(TuiTeX.rightAlign(x, 2) + ". " + list[x - 1]);
        }
	System.out.println();
    }

    public static void enumerate(String title, ArrayList<String> list)
    {
	System.out.println();
	ul(title);
        if(list.size() == 0) System.out.println(" [Empty list]");
	else {
	    for(int x = 1; x <= list.size(); x++){
	        System.out.println(TuiTeX.rightAlign(x, 2) + ". " + list.get(x - 1));
            }
	    System.out.println();
	}
    }
}
