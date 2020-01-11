import math
import copy
import inc_shortest_paths as dijkstra

# I am hardcoding for a single possible start node
class BTCandidate():
	def __init__(self, goalName, parentBTN, distance):
		self.gn = goalName
		self.p = parentBTN
		self.d = distance

class BTNode():
	def __init__(self, goalName, loc, parent, distance):
		self.goalName = goalName #string
		self.location = loc#String
		self.extGoalNames = [] # list of strings
		self.parent = parent #BTNode
		self.distance = distance #int
	
	# bypass the defaul call by reference	
	def newExtList(self, oldExt):
		for i in oldExt:
			if(i != self.goalName):
				self.extGoalNames.append(i)
	
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
		
		# for results ~ printout number of expansions/selections
		self.expansions = 0
		self.steps = 0		
	
	def expand(self):
		# always expand before stepping.
		# always expand the selected node.
		self.expansions += 1
		
		# measure distance to all exterior goal nodes from BTT selection
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
		
	def step(self):
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
		# this function removes the current coal from ext list
		next.newExtList(closestCandidate.p.extGoalNames)
		#print("stepping...", next.extGoalNames)
		#print("stepping...", closestCandidate.p.extGoalNames)
		#print("stepping...", closestCandidate.gn)

		# check for new exterior goal nodes and add 'em in
		for n in self.goals.goalDict[closestCandidate.gn].post:
			# each parent goal of the selected goal
			if(self.goals.goalDict[n].isExterior(next.extGoalNames)):
				#print("is exterior: ", n)
				next.extGoalNames.append(n)
		
		# check for completion
		complete = False
		self.steps += 1
		if(next.extGoalNames == []):
			addDist = next.distance - next.parent.distance
			msg = "STEP " + str(self.steps) + ":\nmove from " + next.parent.goalName + " to " + next.goalName + " for " + str(addDist) + ".\n"
			msg += "Complete: No more exterior nodes in " + str(self.steps) + " steps."
			complete = True
		else:
			addDist = next.distance - next.parent.distance
			msg = "~"
			msg += "STEP " + str(self.steps) + ":\nmoves from " + next.parent.goalName + " to " + next.goalName + " for " + str(addDist) + ".\n"

		# update the selected node for expansion
		self.selection = next
		
		# ? testing ?
		#print(msg)
		return complete
	
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
