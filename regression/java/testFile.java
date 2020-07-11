import java.util.*;

public class testFile {
	public static void main(String [] args) {
		Team t = new Team("JJ Burke",127);
		
		System.out.println(t.getName());
		Random ran = new Random();
		System.out.println(ran.nextGaussian());
		System.out.println(ran.nextGaussian());
	}
	
}