//https://github.com/CyberLemonade/Codingame/blob/master/Very%20Hard/The%20Resistance.java
import java.util.*;
class Solution {

    static String morse[] = {".-","-...","-.-.","-..",".",
                             "..-.","--.","....","..",".---",
                             "-.-",".-..","--","-.","---",
                             ".--.","--.-",".-.","...","-",
                             "..-","...-",".--","-..-","-.--","--..",};

    static String sequence = "";
    static Map<String,Integer> occur = new HashMap<String,Integer>();
    static long[] combos;
    static int max = 0;

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        sequence = in.nextLine();
        int N = in.nextInt();
        combos = new long[sequence.length()];
        in.nextLine();
        for (int i = 0; i < N; i++) {
            morph(in.nextLine());
        }
        System.out.println(tryCombos(0));
    }

    public static void morph(String word) {
        String morphed = "";
        for (int i = 0; i < word.length(); i++) {
            morphed += morse[word.charAt(i)-65];
            if (sequence.indexOf(morphed)==-1) {return;}
        }
        int freq = 1;
        try {freq+=occur.get(morphed);}
        catch (Exception e) {max=Math.max(max,morphed.length());}
        occur.put(morphed,freq);
    }

    public static long tryCombos(int start) {
        if (start==sequence.length()) return 1L;
        if (combos[start]!=0) return combos[start]-1L;
        long result = 0;
        for (int i = 1; i<=max && start+i<=sequence.length(); i++) {
            try {
                result += (long)occur.get(sequence.substring(start,start+i))*tryCombos(start+i);
            }
            catch (Exception e) {}
        }
        combos[start] = result+1L;
        return result;
    }
}