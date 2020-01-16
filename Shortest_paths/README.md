# README
This project is based on Dijkstra's Shortest Path algorith (DSP) which is well known. I didn't use an efficient implementation of DSP that relies on min-heaps. For an optimized python implementation of DSP, search elsewhere.
I made this implementation from memory as a warm-up challenge.
This readme is incomplete and the project isn't currently running.
Check back later for updates.
---
## Version 1.0
Version 1.0 implements a nifty data structure based on backtracking trees (see inc_backtracking_tree.py). The effect of this algorithm is to complete a DSP for a set of goals, where each goal has a location on the undirected edge-weighted graph. The algorithm loads graph data and goal data from text files (see edges.txt and expample0.txt). To summarize the algorithm in Version 1.0, it completes DSP on a set of goals where each goal has prerequisite and postrequisite goals. For example, if there are two goals goal_A and goal_B located at nodes A and B respectively, and goal_A is prerequisite to goal_B, the algorithm will output the shortest path to B that travels through A. To trace the code and see details of how to format the input files, start in main.py. 
---
Note to self, search for "~~~" in files to find areas that need work.
I am in the middle of adding a completedGoals list to each BTNode, and I have to override the call-by-reference in python. I will use that list for checking when prerequisites have been satisfied for tier-1 goals gnomesayin' ;)
