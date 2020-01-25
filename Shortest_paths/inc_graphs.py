# V1.2 Moving variables .distance and .prev to the algorithm itself
# ... Dijkstra's Shortest Path Algorithm inc_shortest_paths.py
# V1.3 Updating for directed graphs

# UndirectedGraphNode has weighted edges
class UndirectedGraphNode:
    def __init__(self, name):
        self.adjList = {}
        self.name = name

    def addAdj(self, name, weight):
        self.adjList[name] = int(weight)

# Edge-weighted undirected graph object where each node has a unique string ID
class UndirectedGraph:
    def __init__(self, edgeList):
        self.nodeNames = []
        self.nodes = {}

        # For each line in the edgeList,
        # one edge per line with 3 tokens, the names of each node and the weight
        for line in edgeList:
            tokens = line.split()
            self.newNode(tokens[0])
            self.newNode(tokens[1])
            self.newAdj(tokens[0], tokens[1], tokens[2])

    # add a name to self.nodeNames if it is not a duplicate
    def newNode(self, node):
        for x in self.nodeNames:
            if(node == x):
                return
        self.nodeNames.append(node)
        self.nodes[node] = UndirectedGraphNode(node)

    # requires only one edge between each pair of nodes
    def newAdj(self, n1, n2, w):
        self.nodes[n1].addAdj(n2, w)
        self.nodes[n2].addAdj(n1, w)

    def weight(self, n1, n2):
        return self.nodes[n1].adjList[n2]