import math

class GraphNode:
	def __init__(self, name):
		self.adjList = {}
		self.name = name
	def addAdj(self, name, weight):
		self.adjList[name] = int(weight)
	
class Graph:
	def __init__(self):
		self.nodeNames = []
		self.nodes = {}
	
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


print("Welcome to Dijkstra's algorithm\n")

edgeListFilename = input("EdgeList Filename: ") #edges.txt
start = input("Start node name: ")
goal = input("Goal node name: ")

edgeFile = open(edgeListFilename, "r", 1)
contents = edgeFile.readlines()

edgeList = []
unvisited = []
distance = {
	start: 0,
	goal: math.inf
}

# create the adjacency list of node names for each node object
# to do this I use a Graph object and fill it with node objects adjkists
g = Graph()

for line in contents:
	tokens = line.split()
	distance[tokens[0]] = math.inf
	distance[tokens[1]] = math.inf
	# only create a new node if the string don't match
	g.newNode(tokens[0])
	g.newNode(tokens[1])
	g.newAdj(tokens[0], tokens[1], tokens[2])
	
# create the unvisited list of strings (node names), then rm start node from the list
# I only remove start here because I initialize the n - just see it.
unvisited = list(distance.keys())
unvisited.remove(start)

distance[start] = 0
currentNode = g.nodes[start]

while(True):
	#update distance
	for x in list(currentNode.adjList.keys()):
		if(distance[currentNode.name] + g.weight(currentNode.name, x) < distance[x]):
			distance[x] = distance[currentNode.name] + g.weight(currentNode.name, x)

	#move to the closest unvisited node
	minDist = math.inf
	candidate = "__FAIL__"
	for x in unvisited:
		if(distance[x] < minDist):
			candidate = x
			minDist = distance[x]

	if(candidate == "__FAIL__"):
		print("There is no path between the specified nodes.")
		quit()	
	# visit the selected node and check for completion
	unvisited.remove(candidate)		
	if(candidate == goal):
		print("The shortest distance from ", start, " to ", goal, " is ", distance[candidate])
		quit()
	currentNode = g.nodes[candidate]


