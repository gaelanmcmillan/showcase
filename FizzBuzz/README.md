# FizzBuzz Readme
This project directory contains examples of FizzBuzz. There are many ways to solve FizzBuzz and it is a simple problem. I have included the correct results in a file, "solution.txt."
I have also included a program for comparing file contents, so that I can quickly check when I have the right output. The source is in "checkSolution.c"

## Purpose
To explore syntax and semantics in various prevalent programming languages and scripting languages in a Windows 10 VS Code environment. The purpose of this project is not to prove optimality of any solution or to optimize any of the solutions.
The following languages are on my hit-list: Haskell, Ruby, Python, Java, Javascript, C, C++, and C#.

## FizzBuzz Problem Definition 
To solve FizzBuzz, write a program that prints out the numbers 1 to 100, with one number per line.   
Exceptions:   
If any number is divisible by 3, print "Fizz" instead.  
If any number is divisible by 5, print "Buzz" instead.  
If any number is divisible by both 3 and 5, print "FizzBuzz."  
To see what a correct solution looks like, refer to the file, "solution.txt"

## File Reference
What follows is a list of all the FizzBuzz source files in this directory. The list item has compilation notes or notes about development that are not commented into the files themselves.

### solution.txt
The correct solution is stored in a data file called solution.txt.

### checkSolution.c
Compile with "g++ checkSolution.c -o checkSolution"
Run the file with arguments to compare the contents of two files, "./checkSolution output.txt solution.txt" 
where "output" is the name of the result being tested against the correct solution contained in "solution.txt".
I have tested this program and it works by comparing the contents of each line in each file until there is a difference in one of the lines, if there is a difference.
Therefore the output must be formatted in the same format as "solution.txt".

### FizzBuzz.c
Compile with "gc FizzBuzz.c -o FizzBuzz"
Delete file in local directory, "output.txt"
Run, "./FizzBuzz" to create a new output text file.
Run, "./checkSolution output.txt solution.txt"
Console outputs, "The solution is correct."

### FizzBuzz.cpp
Compile with "g++ FizzBuzz.cpp -o FizzBuzz"
Run, "./FizzBuzz >> output.txt"

### FizzBuzz.java
DEPRECATED
Compile with "javac FizzBuzz.java"
Run with "java FizzBuzz"
FizzBuzz.java outputs to the console.
Note to self, if I run this file using the command-line, then I can't have a line, "package FizzBuzz." If I compile and run using the IDE, then I need to include "package FizzBuzz."
VSCode produces an annoying red text whenever I remove the package.

