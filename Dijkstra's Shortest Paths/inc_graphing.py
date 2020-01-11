import math

# A GraphNode is a location on the world map
class GraphNode:
	def __init__(self, name):
		self.adjList = {}
		self.name = name
	def addAdj(self, name, weight):
		self.adjList[name] = int(weight)

# A Graph object stores the world map for doing Dijkstra's Algorithm
class Graph:
	def __init__(self):
		self.nodeNames = []
		self.nodes = {}
		self.distance = {}
		self.prev = {}
	# manual uniqueness checking...?
	def newNode(self, node):
		for x in self.nodeNames:
			if(node == x):
				return
		self.nodeNames.append(node)
		self.nodes[node] = GraphNode(node)
	
	# requires only one edge between each pair of nodes
	def newAdj(self, n1, n2, w):
		self.nodes[n1].addAdj(n2, w)
		self.nodes[n2].addAdj(n1, w)
		
	def weight(self, n1, n2):
		return self.nodes[n1].adjList[n2]

# read list of undirected edges and return a Graph object
def makeUndirectedGraph(edgeList):
	
	g = Graph()

	for line in edgeList:
		tokens = line.split()
		g.distance[tokens[0]] = math.inf
		g.distance[tokens[1]] = math.inf
		g.prev[tokens[0]] = ""
		g.prev[tokens[1]] = ""
		g.newNode(tokens[0])
		g.newNode(tokens[1])
		g.newAdj(tokens[0], tokens[1], tokens[2])
		
	return g
