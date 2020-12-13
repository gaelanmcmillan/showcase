# Backtracking Recursion Readme
## Project Description
The purpose of this project is to create two backtracking algorithms to solve the nxn queens problem. 
One algorithm will be written in C with structs, and the other algorithm will be written in C++ with classes.

## nxn Queens, Backtracking Algorithms, and CSP
Backtracking algorithms are used to solve Constraint Satisfaction Problems (CSP), and nxn Queens is a CSP. For a problem to be CSP, it can be written as the problem of assigning variables to domains according to a set of constrains. In nxn Queeens, the problem is to put n queens on an nxn chess board such that no queens are attacking each other according to the rules of chess. In this project I will find all solutions for nxn queens . With respect to CSP, the variables are the queens, the domains are the squares on the board, and the constraint is that no queen can be placed in attacking range of any other. To simplify the interface for this problem, the value n will be hardcoded into the source files, and the output to the console will be the total number of solutions. I will be solving nxnQueens as an enumeration problem, then testing for increasing values of n and recording the results.

## 

## Source Files
### Activity Log
activityLog.txt
The activity log is filled with numbered entries that record progress in the completion of this project.
### C Solution with Datastructures
nxnQueens.c
The input variable n, for nxn queens is hard-coded into the source file, #define N 8, for example. 
To compile the source file enter,
    "gcc nxnQueens.c -o cQueens"
To run the program enter,
    "./cQueens"
### C++ Solution with Classes
nxnQueens.cpp
The input variable n, for nxn queens is hard-coded into the source file, #define N 8, for example. Therefore, no command-line arguments are needed.
To compile the source file,
    "g++ nxnQueens.cpp -o cppQueens"
To run the program,
    "./cppQueens"
