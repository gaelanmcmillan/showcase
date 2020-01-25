# V 1.0 Each goal node location must be visited to stop the algorithm
# V 1.1 Some goals require visiting only 1 of 2 or more locations (mutual goals)
# V 1.2 Import Optional Goals from a separate file
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
	
	#  given a list of completed goals, return True when all prerequisites are complete
	def isExterior(self, completedGoals):
		# for each list of strings...
		for prereq in self.pre:
			# for each mutual goal...
			for goalName in prereq:
				# at least one must be complete.
				if(goalName in completedGoals):
					break
				return False
		return True

# Goals objects are not replicated for each BTNode.
# the BTNode just stores a list of exterior nodes. 
class Goals():
	def __init__(self, fileContents):
			self.ext = [] # These are the exterior nodes to START with ONLY.
			self.goalDict = {} # this is a heavy datadtructure for referencing goalNodes with strings.

			# initiate each goal with name and location
			for line in fileContents:
				tok = line.split()
				#instanciate each goal w/ name and location
				self.goalDict[tok[0]] = GoalNode(tok[0], tok[1])
	
			# parse each line into the goalNode objects in goalDict
			for line in fileContents:
				self.makeGoalNode(line)


	# Given a line of Goals input and an initialized goalDict with name and location,
	# parse the line data into a goalNode object: String --> post, pre, isOptional.
	# Add the exterior goals to self.ext.
	# where "this goal" (in comments) is the goal being made.
	# As of V.1.2, 2020-1-19,
	# the 0th token on the line is the goal name
	# the 1st token on the line is the location name
	# the remaining tokens are the names of the prerequisites
	def makeGoalNode(self, current):
		# tokenize the input string for this goal
		tok = current.split()

		# if this goal has no prerequisites...
		if(len(tok) == 2):
			# set this goal as exterior 
			self.ext.append(tok[0])

		# for each prerequisite token
		for t in range(2, len(tok)):
			# prerequisite goals a OR b OR c is denoted by "a|b|c"
			# any token could contain this key character: "|"
			listMutualGoals = tok[t].split('|')

			# for each prerequisite goal in the token...
			for prereqGoal in listMutualGoals:
				# add "this goal" to the postrequisites of the prerequisite goal
				self.goalDict[prereqGoal].post.append(tok[0])

			# goals are only mutual with respect to the given postrequisite
			# goalDict[tok[0]].pre is a list of lists of strings
			# each list of strings in pre is a list of mutual goals as in "a|b|c"
			self.goalDict[tok[0]].pre.append(listMutualGoals)
	