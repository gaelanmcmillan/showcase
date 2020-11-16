/*
 *  Name: nxnQueens.c
 *  Date: Started 2020-Nov-15
 *  Author: Andrew Meijer
 *  Purpose: Create backtracking recursion with datastructures
 */

#define N 4
#include <stdio.h>

struct BTNode {
    struct BTNode parent;
    struct BTNode children[N];
    char board[N][N];

};

int main(){

    return 0;
}