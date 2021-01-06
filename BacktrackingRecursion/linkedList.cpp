//NAME: linkedlist.cpp
//PURPOSE: Create a linked list node object that points to other linked list node objects. Create a linked list out of node objects and traverse it.
//AUTHOR: Andrew Meijer (with help from the internet!)
//DATE: January 6, 2021

#include <cstddef>
#include <iostream>

#define dataSize 10

using namespace std;

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