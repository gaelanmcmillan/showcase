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
prev = {}

# create the adjacency list of node names for each node object
# to do this I use a Graph object and fill it with node objects adjlists
g = Graph()

for line in contents:
	tokens = line.split()
	distance[tokens[0]] = math.inf
	distance[tokens[1]] = math.inf
	prev[tokens[0]] = ""
	prev[tokens[1]] = ""
	# only create a new node if the string don't match
	g.newNode(tokens[0])
	g.newNode(tokens[1])
	g.newAdj(tokens[0], tokens[1], tokens[2])
	
# create the unvisited list of strings (node names), then rm start node from the list
# I only remove start here because I initialize the n - just see it.
unvisited = list(distance.keys())
unvisited.remove(start)

distance[start] = 0
#arbitrary prev value for prev[start
prev[start] = start
currentNode = g.nodes[start]

while(True):
	#update distance
	#for each adacent node
	for x in list(currentNode.adjList.keys()):
		if(distance[currentNode.name] + g.weight(currentNode.name,x) < distance[x]):
			distance[x] = distance[currentNode.name] + g.weight(currentNode.name, x)
			prev[x] = currentNode.name
	
	#select the closest unvisited node
	minDist = math.inf
	candidate = "__FAIL__"
	for x in unvisited:
		if(distance[x] < minDist):
			candidate = x
			minDist = distance[x]
	
	# check for unselectability
	if(candidate == "__FAIL__"):
		print("There is no path between the specified nodes.")
		quit()	
	
	# visit the selected node
	unvisited.remove(candidate)		
	currentNode = g.nodes[candidate]
	
	# check for completion
	if(currentNode.name == goal):
		# test the solution
		print("The shortest distance from ", start, " to ", goal, " is ", distance[currentNode.name], ".")
		
		# test the prev values
		printout = []
		trav = goal
		travsize = 0
		while trav != start:
			trav = prev[trav]
			travsize += 1
			printout.append(trav)
		printout.reverse()
		jankyFlag = True
		for i in printout: 
			if(jankyFlag):
				jankyFlag = False
				previousIndex = i
			else:
				print("Move from ", previousIndex, " to ", i, " for ", g.weight(previousIndex, i))
				previousIndex = i
		print("Move from ", previousIndex, " to ", goal, " for ", g.weight(previousIndex, goal))
		quit()