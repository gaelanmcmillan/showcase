import math

# g is the graph, t is a list of goal objects, and s is sttart location
def simulPaths(g, t, s):
	# Dijkstra's Algorithm
	unvisited = []
	unvisited = list(g.distance.keys())
	unvisited.remove(s)
	
	for i in g.distance:
		g.distance[i] = math.inf
	g.distance[s] = 0

	for i in g.prev:
		g.prev[i] = ""
	#mandatory false prev value for prev[start]
	g.prev[s] = s
	
	# return distances to goal locations
	r = {}
	for x in t:
		r[x.name] = math.inf
	
	currentNode = g.nodes[s]
	
	while(unvisited != []):
		#update distance for each adjacent node
		for x in list(currentNode.adjList.keys()):
			if(g.distance[currentNode.name] + g.weight(currentNode.name,x) < g.distance[x]):
				g.distance[x] = g.distance[currentNode.name] + g.weight(currentNode.name, x)
				g.prev[x] = currentNode.name

		#select the closest unvisited node
		minDist = math.inf
		candidate = "__SOUND__"
		for x in unvisited:
			if(g.distance[x] < minDist):
				candidate = x
				minDist = g.distance[x]
		
		# check for unselectability
		if(candidate == "__SOUND__"):
			print("ERROR: in file inc_shortest_paths.py  . . .")
			print("There is no path between the specified nodes.")
			quit()	
	
		# visit the selected node
		unvisited.remove(candidate)		
		currentNode = g.nodes[candidate]
		
		# check for completion
		# t stands for sinks, r is resturlnts.
		for x in t:
			if(currentNode.name == x.location):
				r[x.name] = g.distance[x.location]
				t.remove(x)
				if(t == []):
					return r