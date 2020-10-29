//NAME: CheckSolution.c
//DATE: 1/29/2020
//AUTHOR: Andrew Meijer
//PURPOSE: Compare two files for FizzBuzz solution checking.
//         Include the filenames as arguments.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]){
    if(argc != 3){
        printf("Incorrect arguments.");
        exit(0);
    }

    FILE *f1p;
    FILE *f2p;

    char f1LineContents[255];
    char f2LineContents[255];

    f1p = fopen(argv[1], "r");
    f2p = fopen(argv[2], "r");

    // store the result of strcmp
    int comparison = 0;
    // error line in case the files are unidentical
    int flag = 0;

    for(int i=0; i<100; i++){
        fscanf(f1p, "%s", f1LineContents);
        fscanf(f2p, "%s", f2LineContents);
        comparison = strcmp(f1LineContents, f2LineContents);
        if(comparison != 0){
            flag = i+1;
            break;
        }
    }

    fclose(f1p);
    fclose(f2p);

    if(flag == 0){
        printf("The solution is correct.\n");
    }else{
        printf("The solution is incorrect on line %d.\n", flag);
    }
}