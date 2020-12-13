/*
 *  Name: nxnQueens.c
 *  Date: Started 2020-Nov-15
 *      2020-Dec-07:
 *          Adding nested structure; 
 *          Implementing algorithm - backtracking enumeration;
 *          This is a recursive algorithm.
 *  Author: Andrew Meijer
 *  Purpose: Create backtracking recursion with datastructures
 */

#define N 4
#include <stdio.h>

struct BTNode {
    int h; //the current row in the algorithm
    struct BTNode* p; //pointer to the parent of this node
    struct BTNode* c[N]; //pointers to child nodes
    char board[N][N]; //in board[x][y]: x = h, y = c[i] where i={0,1,2,3}.
};

//BTNode c for candidate; checks for horizontal collision
char horizontal(BTNode cx){
    
}

char diagonal(BTNode cx){

}

int main(){
    
    return 0;
}