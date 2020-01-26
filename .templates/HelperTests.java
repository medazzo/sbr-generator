package {{package}} ;
 

import java.security.SecureRandom;

public class HelperTests {
    
    private static final String CHAR_LOWER = "abcdefghijklmnopqrstuvwxyz";
    private static final String CHAR_UPPER = CHAR_LOWER.toUpperCase();
    private static final String NUMBER = "0123456789";
    private static final String DATA_FOR_RANDOM_STRING = CHAR_LOWER + CHAR_UPPER + NUMBER;
    private static SecureRandom random = new SecureRandom();

    public static int randomInteger(int bound) {
        return  random.nextInt(bound);        
    }
    
    public static double randomdouble() {        
        return  Math.random();        
    }
        
    public static String randomString(int length) {
        if (length < 1) throw new IllegalArgumentException();

        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
			// 0-62 (exclusive), random returns 0-61
            int rndCharAt = random.nextInt(DATA_FOR_RANDOM_STRING.length());
            char rndChar = DATA_FOR_RANDOM_STRING.charAt(rndCharAt);
            sb.append(rndChar);

        }

        return sb.toString();

    }
    public static String randomMail() {
        return randomString(10)+"@"+randomString(7)+".com";

    }
 
}
