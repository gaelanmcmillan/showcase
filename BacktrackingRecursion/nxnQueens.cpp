/*
 *  Name: nxnQueens.cpp
 *  Date: Started 2020-Nov-15
 *  Author: Andrew Meijer
 *  Purpose: Create backtracking recursion with classes
 */

#define N 4
#include <vector>
#include <iostream>

using namespace std;

class BTNode {
    public:
        BTNode* children[N];
        vector<int> board;
        
        BTNode() {
            for(int i = 0; i<N; i++){
                board[i] = -1;
            }            
        }
        BTNode(vector<int> parentBoard) {
            //board deep copies parentBoard
            for(int i=0; i<N; i++){
                board[i] = parentBoard[i];
            }
        }
};

//place a queen in each row for each child node; 
//test if each node passes horizontal and diagonal; 
//expand each node that passes
vector<vector<int> > expand(BTNode root){
    for(int i=0; i<N; i++){
        
    }
}

//return true of any queens are attacking each other horizontally
bool horizontal(vector<int> board, int col){
    //if any board values are equal, there is a horizontal collision
    for(int i=0; i<col; i++){
        if(board[col] == board[i]){
            return true;
        }            
    }
    return false;
}

/*
diagonal(board, 2);
vector<int> {0, 2, 2, -1}
       |
   x   v
   0 1 2 3
0  x O O O
1  O x O O
2  O O 0 O
3  O O x O

b[col] = 2
if(b[col-1] == 1 || b[col-1] == 3){ that's bad}
*/

//return true if any queens are attacking each other diagonally

bool diagonal(vector<int> board, int col){

    int check = col-1;
    int expectedDifference = 0;
    for (int j = 0; j <= check; j++){
        expectedDifference = check-j;
        cout<<"board place being checked against: "<<check<<" value: "<<board[check]<<endl;
        cout<<"board place being checked: "<<j<<" value: "<<board[j]<<endl;
        cout<<"expected value: "<<check-expectedDifference<<" or "<<check+expectedDifference<<endl;
        if (board[j] == check-expectedDifference || board[j] == check-expectedDifference){
            return true;
        }
        cout<<""<<endl;
    }
    return false;
    //board[col];
}

int main(){
    // BTNode root = new BTNode();

    // vector<vector<int> > solutions = expand(root);
    vector<int> board;
    board.push_back(0);
    board.push_back(2);
    board.push_back(2);
    board.push_back(-1);
    bool v = diagonalTwo(board, 3);

    cout << v << endl;

    return 0;
}

/* LINKED LIST CODE *

//Linked List Node object
class LLNode{
    public:
        int data;
    LLNode * next;
};


//in the traversal, data from each node is printed as evidence
void traverse(LLNode * n){
    while(n != NULL){
        cout << n->data << " ";
        n = n->next;
    }
}

int main(){
    int dataset[dataSize] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}; 

    LLNode * nodes[dataSize];

    for(int i=0; i<10; i++){
        nodes[i] = new LLNode();
        nodes[i]->data = dataset[i];
    }

    //Two loops  is still linear time
    for(int i=0; i<9; i++){
        nodes[i]->next = nodes[i+1];
    }
    nodes[9]->next = NULL;

    traverse(nodes[0]);
    return 0;
}
*/



