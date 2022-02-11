import java.util.*;
import java.lang.*;
import java.io.*;


public class Main {
    static Scanner sc;


    static void solution() throws Exception {
        // Solution {N}
    }


    public static void main(String[] args) throws Exception {
        InputStream is = System.in;
        PrintStream ps = System.out;
        try {
            if (System.getProperty("ONLINE_JUDGE") == null) {
                is = new FileInputStream(".cpl_files/{N}.in.txt");
                ps = new PrintStream(".cpl_files/{N}.out.txt");
            }
        } catch (Exception e) {}
        sc = new Scanner(is);
        System.setOut(ps);
        int t;
        t = sc.nextInt();
        while (t-- > 0) {
            solution();
        }
        is.close();
        ps.close();
    }
}
