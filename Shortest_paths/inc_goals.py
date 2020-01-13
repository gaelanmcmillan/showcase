# V 1.0 Each goal node location must be visited to stop the algorithm
# V 1.1 Some goals require visiting only 1 of 2 or more locations
# V 1.2 Some goals are optional 
class GoalNode:
	def __init__(self, id, l):
		# identification
		self.name = id
		self.location = l		
		# list of postrequisite goals
		self.post = []
		# prerequisite goals
		self.pre = []
		self.isOptional = False
		# for optional goals,
		# cord contains the list of other goals i.e. a|b
		self.cord = []
	
	# given a list of completed goals, is this goal now exterior
	def isExterior(self, incompleteExt):
		for prereq in self.pre:
			if(prereq in incompleteExt):
				return False
		return True

# Goals objects are not replicated for each BTNode.
# the BTNode just stores a list of exterior nodes. 
class Goals():
	def __init__(self):
			self.ext = [] # This variable might be useless. *needs review
			self.goalDict = {}

	def makeGoalNode(self, current):
		tok = current.split()
		if(len(tok) == 2):
			self.ext.append(tok[0])
		# for each prerequisite token
		for t in range(2, len(tok)):
			# prerequisite goal_a OR goal_b is denoted with "goal_a|goal_b"
			# any token could contain this key character: "|"
			t_sub = tok[t].split('|')
			for cor in t_sub:
				self.goalDict[tok[0]].pre.append(cor)
				self.goalDict[cor].post.append(tok[0])
				self.goalDict[cor] # YIKES. Consider a different aproach...
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