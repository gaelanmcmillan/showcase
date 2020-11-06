/*
NAME:       FizzBuzz.cpp
DATE:       2020/11/05
AUTHOR:     Andrew Meijer
PURPOSE:    Print the FizzBuzz solution to standard output.
*/

#include <iostream>

//observe my recursive method.
int fizzBuzz(int n, short f) {

    f = 0;
    
    if(n % 3 == 0){
        std::cout << "Fizz";
        f = 1;
    }

    if(n % 5 == 0){
        std::cout << "Buzz";
        f = 1;
    }
    
    if(f == 0){
        std::cout << n;
    }

    std::cout << "\n";

    //exit condition
    if(n == 100){
        return 0;
    }

    n = n+1;
    //Why pass the flag f? I am not sure how memory allocation is done for when I only need one flag at a time. I felt funny writing "int f" because I don't need a new flag. The only instances of this function stay open for all 100 even though I am not backtracking, so this is a weird algorithm. I need to think more about the different between interation and recursion. I remember learning in school that Haskell can't do iteration.
    fizzBuzz(n, f);
    return 0;
}


int main() {

    fizzBuzz(1, 0);
    return 0;
}

