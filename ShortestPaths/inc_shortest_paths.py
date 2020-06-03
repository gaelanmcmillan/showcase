# V1.2 Moving variables .distance and .prev over from inc_graphs.py
# V1.3 Updating for directed graphs

import math
# import inc_graphs as graphs

# g is the graph, t is a list of goal objects, and s is start location (string)
# goal objects have variables .name and .location, where .location is in the graph g
# t can be modified but not g or s
# return a dictionary indexed by goalNames storing the distances to each goal.
def simulPaths(g, t, s):
	# Dijkstra's Algorithm
	distance = {}
	prev = {} # store the paths if you want
	unvisited = []

	# initialize wrt graph g
	for n in g.nodeNames:
		distance[n] = math.inf
		prev[n] = ""
		unvisited.append(n)

	# distance is zero at the start
	distance[s] = 0
	# mandatory false prev value for prev[start]
	prev[s] = s
	# remove start node from unvisited nodes
	unvisited.remove(s)
	
	# r is the results dictionary
	r = {}
	for gol in t:
		r[gol.name] = math.inf
	
	# GraphNode object has .name and dictionary .adjList
	currentNode = g.nodes[s]

	# Important Case: goal node is at start node
	for gol in t:
		if(currentNode.name == gol.location):
			r[gol.name] = 0 # distance 0
			t.remove(gol)
			# Check for completion
			if(t == []):
				return r

	while(unvisited != []):
		# update distance for each adjacent node
		for x in list(currentNode.adjList.keys()):
			if(distance[currentNode.name] + g.weight(currentNode.name,x) < distance[x]):
				distance[x] = distance[currentNode.name] + g.weight(currentNode.name, x)
				prev[x] = currentNode.name

		#select the closest unvisited node
		minDist = math.inf
		candidate = "__SOUND__"
		for x in unvisited:
			if(distance[x] < minDist):
				candidate = x
				minDist = distance[x]
		
		# check for unselectability
		if(candidate == "__SOUND__"):
			print("ERROR: in file inc_shortest_paths.py  . . .")
			print("There is no path between the specified nodes.")
			quit()	
	
		# visit the selected node
		unvisited.remove(candidate)		
		currentNode = g.nodes[candidate]
		
		# check for completion
		# t stands for sinks, r is results.
		for gol in t:
			if(currentNode.name == gol.location):
				r[gol.name] = distance[gol.location]
				t.remove(gol)
				if(t == []):
					return r
	print("ERROR: in file inc_shortest_paths.py  . . .")
	print("All nodes have been visited.")
	quit()
