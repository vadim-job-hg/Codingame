import java.util.*;
import java.io.*;
import java.math.*;
import java.awt.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Solution {

    static int seen = 0;
    static int N;
    static Point[] spots;
    static boolean[] used;
    static double path = 0.0;

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        //System.out.println("ENTER:");
        N = in.nextInt();
        spots = new Point[N];
        used = new boolean[N];
        for (int i = 0; i < N; i++) {
            int X = in.nextInt();
            int Y = in.nextInt();
            spots[i] = new Point(X,Y);
        }

        findPath(0);

        // Write an action using System.out.println()
        // To debug: System.err.println("Debug messages...");

        System.out.println((int)(Math.round(path)));
    }

    public static void findPath(int index) {
        used[index] = true;
        Point p = spots[index];
        double minDist = Integer.MAX_VALUE;
        int ind = 0;
        for (int i = 0; i < N; i++) {
            if (!used[i]&&i!=index) {
                double Dist = Math.sqrt(Math.pow(p.x-spots[i].x,2)+Math.pow(p.y-spots[i].y,2));
                if (Dist<minDist) {
                    minDist = Dist;
                    ind = i;
                }
            }
        }
        if (ind==0) {minDist = Math.sqrt(Math.pow(p.x-spots[0].x,2)+Math.pow(p.y-spots[0].y,2));}
        System.err.println("Nearest point to "+index+" is "+ind);
        seen++;
        path += minDist;
        System.err.println("Path is "+path);
        used[ind] = true;
        if (seen!=N) {findPath(ind);}
    }
}