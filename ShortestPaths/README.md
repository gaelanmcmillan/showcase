# README Version 1.2
This project is based on Dijkstra's Shortest Path algorith (DSP) which is well known. 
This readme for version 1.2 will include a brief summary of all the files included in this directory.

### main.py
main.py is the first script to run. It imports the other files, initializes the datastructures, and runs tests to visualize the results on the terminal. The current test involves running the step and expand functions in in_backtracking_tre.py, and then displaying the solution. To run the project, navigate to this directory and use the command, "python main.py."

### inc_graphs.py
inc_graphs.py has functions and classes for implementing an edge-weighted undirected graph.

### inc_goals.py
inc_goals.py has functions and classes for implementing a datastructure that stores goal locations for the algorithm to visit on the graph. Each goal may have one or more prerequisites and one or more postrequisites. New in V1.2 is that goals can also have prerequisites where exactly one of many goals is required to satisfy the prerequisite. I call this "OR-functionality" or "mutual goals," albeit "mutual" is a bad name for this functionality.

### inc_shortest_paths.py
inc_shortest_paths implements Dijkstra's Algorithm.

### inc_backtracking_tree.py
inc_backtracking_tree.py implements the algorithm by building a atastructure that is like a backtracking tree. Perhaps this file is poorly named because I don't remember if the structure is exactly a BT tree or not. I need to look into it.

### edges.txt
edges.txt is an example for inputting an undirected edge-weighted graph. Most of my examples run on this graph because it is easy to remember and not too simple.

### example0.txt
example0.txt is a test example for inputting a goals datastructure.

### example1.txt
example1.txt

### example2.txt
example2.txt

### example3.txt
example3.txt

### example4.txt
example4.txt
