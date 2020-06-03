# V if needed, add printout for routes between goals

import inc_graphs as graphs
import inc_goals as goals
import inc_backtracking_tree as BT
import inc_shortest_paths as dijkstra

def contentsFromFile(filename):
	f = open(filename, "r", 1)
	contents = f.readlines()
	f.close()
	return contents

print("\n\nWelcome to testing")
edgesFilename = "edges.txt"
goalsFilename = "example4.txt"
start = "s"

'''
# instanciate the datastructures
edgesFilename = input("Name a edge list file: ") #edges.txt
goalsFilename = input("Name a goal list file: ") #examples.txt
start = input("Name a starting node: ")
'''

# instanciate the datastructures
g = graphs.UndirectedGraph(contentsFromFile(edgesFilename))
s = start
t = goals.Goals(contentsFromFile(goalsFilename))

print("\t Graph file: ", edgesFilename)
print("\t Goals file: ", goalsFilename)

# Tests
# ##########################################
'''
# TEST making the datastructures
print the goal structure
print("Exterior Nodes: ", t.ext, "\n")
for x in t.goalDict:
	print("Name:\t\t", t.goalDict[x].name)
	print("Location:\t", t.goalDict[x].location)
	print("Parents:\t", t.goalDict[x].post)
	print("Children:\t", t.goalDict[x].pre, "\n")
'''

'''
# TEST simulPaths, Dijkstra's algorithm inc_shortest_paths.py
searchGoals = []
for gol in t.ext:
	searchGoals.append(t.goalDict[gol])
results = dijkstra.simulPaths(g, searchGoals, s)
for r in results:
	print(r, " : ", results[r])
'''


#traversing the BTTree (and building it)
graphSearch = BT.BTTree(s, t, g)
#step by step, expand then select
done = False # flag
while(not done):
	graphSearch.expand()
	done = graphSearch.step()

graphSearch.displayRoute()
