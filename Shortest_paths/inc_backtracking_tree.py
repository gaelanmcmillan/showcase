import math
import inc_shortest_paths as dijkstra

# I am hardcoding for a single possible start node
class BTCandidate():
	def __init__(self, goalName, parentBTN, distance):
		self.gn = goalName
		self.p = parentBTN
		self.d = distance

class BTNode():
	def __init__(self, goalName, loc, parent, distance):
		self.goalName = goalName # string
		self.location = loc # String
		self.extGoalNames = [] # list of strings
		self.parent = parent # BTNode
		self.distance = distance # int
		self.completedGoals = [] # list of completed goals

	# copy the valuess of the parent list to the new list
	# remove self.goalName from the list
	def newExtList(self, oldExt):
		for i in oldExt:
			if(i != self.goalName):
				self.extGoalNames.append(i)
	
	# copy the values from the parent list to the new list
	# add the current goalName to the list
	def newCompletedGoalsList(self):
		for i in self.parent.completedGoals:
			self.completedGoals.append(i)
		self.completedGoals.append(self.goalName)

class BTTree():
	def __init__(self, start, goals, graph):
		self.root = BTNode("__START__", start, None, 0)
		self.root.newExtList(goals.ext)
		self.graph = graph
		self.selection = self.root
		self.goals = goals
		# each candidate needs a BTNode parent, goalnode name, and distance
		# I created a new object called BTCandidate to store this
		self.candidates = []

		# progress trackers
		self.expansions = 0
		self.steps = 0		
	
	# Create BTCandidate objects and add them to the list self.candidates
	def expand(self):
		# always expand before stepping.
		# always expand the selected node.
		self.expansions += 1
	
		# Use Dijkstra's Algorithm!
		# Measure distance to all exterior goal nodes from BTT selection.
		# store the result
		extGoalObjs = []
		for gnn in self.selection.extGoalNames:
			extGoalObjs.append(self.goals.goalDict[gnn])
		distanceDict = dijkstra.simulPaths(self.graph, extGoalObjs, self.selection.location)

		msg = "EXPANSION " + str(self.expansions) + ":\n"
		msg += "There are " + str(len(distanceDict)) + " new candidate(s) from " + self.selection.goalName + ":\n"
		for ig in distanceDict:
			msg += "goal:" + ig + "\tdistance:" + str(distanceDict[ig]) + "\n"

		# add the distance to each candidate to the distance of their parent
		# create a candidate for each one of these and add each to the BTT list
		for cand in distanceDict:
			distanceDict[cand] += self.selection.distance
			self.candidates.append(BTCandidate(cand, self.selection, distanceDict[cand]))	

		msg += "There are " + str(len(self.candidates)) + " total candidate(s):\n"
		for c in self.candidates:
			msg += c.gn + " from " + c.p.goalName + ": " + str(c.d-c.p.distance) + "\n"
		#print(msg)

		return

	# Produce the next BTTree state by stepping to a 
	# Select a new currentNode from self.candidates and create a BTNode for it; check for completion.	
	def step(self):
		# Expand before each step to produce candidates
		self.steps += 1

		# find the candidate with the shortest distance
		minDist = math.inf
		for cand in self.candidates:
			if(cand.d < minDist):
				minDist = cand.d
				closestCandidate = cand
		
		# remove the found candidate from the candidate list
		self.candidates.remove(closestCandidate)

		# create a new BTNode for the candidate; copy the exterior goals from parent
		next = BTNode(closestCandidate.gn, self.goals.goalDict[closestCandidate.gn].location, closestCandidate.p, closestCandidate.d)
		# pass values to a new extList and remove the current goal
		next.newExtList(closestCandidate.p.extGoalNames)
		# pass values to a new completedGoals list and add the goalName
		next.newCompletedGoalsList()

		#print("stepping...", next.extGoalNames)
		#print("stepping...", closestCandidate.p.extGoalNames)
		#print("stepping...", closestCandidate.gn)

		# check for new exterior goal nodes and add 'em in
		# For each posrequisite (parent) goal of the selected goal...
		for n in self.goals.goalDict[closestCandidate.gn].post:
			if(self.goals.goalDict[n].isExterior(next.completedGoals)):
				next.extGoalNames.append(n)
		
		# V1.3 ~ if more than one candidate has the same location, merge them.

		# update the selected node for expansion
		self.selection = next

		# check for completion
		complete = False
		if(self.isComplete()):
			addDist = next.distance - next.parent.distance
			msg = "STEP " + str(self.steps) + ":\nmove from " + next.parent.goalName + " to " + next.goalName + " for " + str(addDist) + ".\n"
			msg += "Complete: No more exterior nodes in " + str(self.steps) + " steps."
			complete = True
		else:
			addDist = next.distance - next.parent.distance
			msg = "~"
			msg += "STEP " + str(self.steps) + ":\nmoves from " + next.parent.goalName + " to " + next.goalName + " for " + str(addDist) + ".\n"
		
		#print(msg)
		return complete
	
	# Return True if the structure is in a stopping state.
	def isComplete(self):
		if(self.selection.extGoalNames == []):
			return True
		return False

	def displayRoute(self):
		printout = []
		travNode = self.selection
		finalDistance = travNode.distance
		while(travNode.goalName is not "__START__"):
			printout.append("Move from " + travNode.parent.location + " to " + travNode.location + " for " + travNode.goalName + ". (Shortest distance is " + str(travNode.distance-travNode.parent.distance) + ")")
			travNode = travNode.parent
		# display the solution
		print("Shortest distance to reach all goals from", travNode.location, "is", finalDistance)
		printout.reverse()
		for pr in printout:
			print(pr)
