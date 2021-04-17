import java.io.*;

public class DFA
{
    private int[][] G ={
            //0 1 2  3  4  5  6  7  8  9  ,  .  -
        /*0*/{1,1,6,15,15,15,15,15,15,15,15,15,15},
        /*1*/{15,15,15,15,15,15,15,15,15,15,15,2,15},
        /*2*/{3,3,4,3,3,3,3,3,3,3,15,15,15},
        /*3*/{3,3,4,3,3,3,3,3,3,3,15,15,15},
        /*4*/{3,3,4,3,3,5,3,3,3,3,15,15,15},
        /*5*/{5,5,5,5,5,5,5,5,5,5,7,15,15},
        /*6*/{15,15,15,15,15,15,15,15,15,15,7,15,15},
        /*7*/{9,9,10,15,15,15,15,15,15,15,15,15,8},
        /*8*/{9,10,15,15,15,15,15,15,15,15,15,15,15},
        /*9*/{15,15,15,15,15,15,15,15,15,15,15,11,15},
        /*10*/{15,15,15,15,15,15,15,15,15,15,13,15,15},
        /*11*/{12,12,12,12,12,12,12,12,12,12,15,15,15},
        /*12*/{12,12,12,12,12,12,12,12,12,12,13,15,15},
        /*13*/{15,14,14,14,14,15,15,15,15,15,15,15,15},
        /*14*/{15,15,15,15,15,15,15,15,15,15,15,15,15},
        /*15*/{15,15,15,15,15,15,15,15,15,15,15,15,15},
    };

    private FileReader fr;
    private BufferedReader bf;
    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_GREEN = "\u001B[32m";

    public DFA()
    {
        try {
            fr = new FileReader("data.txt");
            bf = new BufferedReader(fr);
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    public int column(char c)
    {
        if(c == ',')
        {
            return 10;
        }

        else if(c == '.')
        {
            return 11;
        }
        else if(c == '-')
        {
            return 12;
        }
        else if(Character.getNumericValue(c) >= 0 && Character.getNumericValue(c) <= 9)
        {
            return Character.getNumericValue(c);
        }
        else return -1;
    }

    public void comprobar()
    {
        String sCadena;
        int state = 0;
        try{
            while ((sCadena = bf.readLine())!=null) {
                state = 0;
                Thread.currentThread().sleep(200);
                for(int i = 0; i < sCadena.length(); i++)
                {
                    state = G[state][this.column(sCadena.charAt(i))];
                    //System.out.println(state);
                }
                
                if(state == 14)
                {
                    System.out.println(sCadena+ANSI_GREEN+" ....ACEPTADO"+ANSI_RESET);
                }
                else{
                    System.out.println(sCadena+ANSI_RED+" ....RECHAZADO"+ANSI_RESET);
                }
             }
        }
        catch(Exception e){}

    }

    public static void main(String[] args) {
        DFA d = new DFA();
        d.comprobar();
    }
}