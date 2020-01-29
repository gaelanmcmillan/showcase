#include<stdio.h>

void fizzBuzz(int i){
    if(i <= 100){
        printf("%d\n", i);
        i = i+1;
        fizzBuzz(i);
    }
}
int main(){
    fizzBuzz(1);
}

