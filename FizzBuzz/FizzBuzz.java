package FizzBuzz;

/*
NAME:       FizzBuzz.java
DATE:       1/29/2020
AUTHOR:     Andrew Meijer
PURPOSE:    Print out numbers 1 to 100. For each number,
        if the number is divisible by 3, print "Fizz."
        If the number is divisible by 5, print "Buzz."
        If the number is divisible by 3 and 5, print "FizzBuzz."
        Otherwise, print the number,
        one number per line.
*/

public class FizzBuzz {
    public static void main(String[] args){
        boolean FizzOrBuzz = false;
        for(int i=1; i <= 100; i++){
            FizzOrBuzz = false;
            if(i % 3 == 0){
                FizzOrBuzz = true;
                System.out.print("Fizz");
            }
            if(i % 5 == 0){
                FizzOrBuzz = true;
                System.out.print("Buzz");
            }
            if(!FizzOrBuzz){
                System.out.print(i);
            }
            System.out.print("\n");
        }
    }
}