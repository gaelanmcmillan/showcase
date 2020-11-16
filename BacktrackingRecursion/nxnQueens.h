/*
 *  Name: nxnQueens.h
 *  Date: Started 2020-Nov-15
 *  Author: Andrew Meijer
 *  Purpose: Declare headers for nxnQueens.c
 *           See Readme for compilation instructions.
 */
struct BTNode {
    struct BTNode parent;
    struct BTNode children[N];
    char board[N][N];

}