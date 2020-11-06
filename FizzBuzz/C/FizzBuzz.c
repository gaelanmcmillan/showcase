/*
NAME:       FizzBuzz.c
DATE:       2020/11/06
AUTHOR:     Andrew Meijer
PURPOSE:    Print the FizzBuzz solution to a file named "output.txt"
*/

#include <stdio.h>

int main() {

    FILE *fp;
    int i = 0;
    short fizz_or_buzz = 1;

    fp = fopen("output.txt", "w+");

    for(i=1; i <=100; i++){
        fizz_or_buzz = 0;

        if(i % 3 == 0){
            fprintf(fp, "Fizz");
            fizz_or_buzz = 1;
        }

        if(i % 5 == 0){
            fprintf(fp, "Buzz");
            fizz_or_buzz = 1;
        }
    
        if(fizz_or_buzz == 0){
            fprintf(fp, "%d", i);
        }
        fprintf(fp, "\n");
    }

    fclose(fp);

}

