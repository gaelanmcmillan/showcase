//NAME: linkedList.c
//PURPOSE: Create a pointer to an array of pointers to LLNode structs in the form of a linked list, and then traverse it.
//AUTHOR: Andrew Meijer 
//DATE: January 4, 2021

#include<stdio.h>
#include<stdlib.h>

# define dataSize 10

struct LLNode {
        int datum;
        struct LLNode * next;
};

//in the traversal, data from each node is printed as evidence
void traverse(struct LLNode * node){
    while(node != NULL){
        printf(" %d ", node->datum);
        node = node->next;
    }
}

int main(){
    //sample data
    int data[dataSize] = {12, 1, 4, 6, 18, 23, 2, 10, 9, 0}; 

    struct LLNode *nodes[dataSize];

    int i=0;
    for(i=0; i<10; i=i+1){
        nodes[i] = NULL;
        nodes[i] = (struct LLNode *)malloc(sizeof(struct LLNode));
        nodes[i]->datum = data[i];
    }

    //Two loops  is still linear time
    for(i=0; i<9; i=i+1){
        nodes[i]->next = nodes[i+1];
    }
    nodes[9]->next = NULL;

    traverse(nodes[0]);
    return 0;
}
