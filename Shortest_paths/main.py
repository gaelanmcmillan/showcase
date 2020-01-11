import inc_graphing as graphs
import inc_goals as goals
import inc_backtracking_tree as BT

def contentsFromFile(filename):
	f = open(filename, "r", 1)
	contents = f.readlines()
	f.close()
	return contents

print("Welcome to testing\n")
'''
edgeListFilename = input("EdgeList Filename: ") #edges.txt
start = input("Start node name: ")
goal = input("Goal node name: ")
'''
# Tests
# ##########################################

#making the goal structure
g = graphs.makeUndirectedGraph(contentsFromFile("edges.txt"))
s = "s"
t = goals.makeGoals(contentsFromFile("example3.txt"))

#print the goal structure
#print("Exterior Nodes: ", t.ext, "\n")
#for x in t.goalDict:
	#print("Name:\t\t", t.goalDict[x].name)
	#print("Location:\t", t.goalDict[x].location)
	#print("Parents:\t", t.goalDict[x].post)
	#print("Children:\t", t.goalDict[x].pre, "\n")

#test 
'''
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