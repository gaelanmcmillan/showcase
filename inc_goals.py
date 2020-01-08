# Each goal node location must be visited to stop the algorithm 
class GoalNode:
	def __init__(self, id, l):
		# identification
		self.name = id
		self.location = l
		
		# list of postrequisite goals
		self.post = []
		# prerequisite goals
		self.pre = []
	
	# given a list of completed goals, is this goal now exterior
	def isExterior(self, incompleteExt):
		for prereq in self.pre:
			if(prereq in incompleteExt):
				return False
		return True

# Originally, the plan was to make this class very light,
# so I could replicate it to each BTNode.
# Now, it is heavy, and the BTNode just stores a list of exterior nodes. 
class Goals():
	def __init__(self):
			# list of exterior nodes
			self.ext = []
			self.goalDict = {}

	def makeGoalNode(self, current):
		tok = current.split()
		if(len(tok) == 2):
			self.ext.append(tok[0])
		for t in range(2, len(tok)):
			# add the listed node to current line's prerequisites
			self.goalDict[tok[0]].pre.append(tok[t])
			# add the current node to listed node's postrequisites
			self.goalDict[tok[t]].post.append(tok[0])
		
# input is space-deliniated, but if one of the tokens is __OR__
# the effect should be to use OR functionality between the tokens on either side.
# One goal per line.
# goalName locationName pre1 pre2 etc...
def makeGoals(fileContents):

	goals = Goals()
	
	for line in fileContents:
		tok = line.split()
		#instanciate each goal w/ name and location
		goals.goalDict[tok[0]] = GoalNode(tok[0], tok[1])
	
	for line in fileContents:
		goals.makeGoalNode(line)
		
	return goals