import java.util.*;
import java.io.*;
import java.math.*;

class Solution
{
    public static void main(String args[])
    {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt(); // the number of temperatures to analyse
        in.nextLine();
        String temps = in.nextLine(); // the n temperatures expressed as integers ranging from -273 to 5526

        int[] arr = new int[n];
        if (n == 0)
            System.out.println(0);
        else
        {
            for (int i = 0; i < n; i++)
            {
                if (temps.indexOf(" ") != -1)
                {
                    arr[i] = Integer.parseInt(temps.substring(0, temps.indexOf(" ")));
                    temps = temps.substring(temps.indexOf(" ") + 1, temps.length());
                }
                else
                {
                    arr[i] = Integer.parseInt(temps);
                    temps = "";
                }
            }

            int max = 0;
            for (int i = 0; i < n; i++)
            {
                if (Math.abs(arr[i]) < Math.abs(arr[max]) || (Math.abs(arr[i]) == Math.abs(arr[max]) && arr[i] > 0))
                    max = i;
            }

            System.out.println(arr[max]);
        }
    }
}