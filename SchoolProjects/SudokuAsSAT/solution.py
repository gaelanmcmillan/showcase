import sys
import os.path #for checking file existence
import formulas #our own file

'''
	Inputting the puzzle:
	The puzzles are encoded as text files
	(described in the assignment pdf)
	To input a text file in this program,
	it must be included as a command-line argument.
	syntax:
		"python solution.py puzzlefile.txt"
	where "puzzlefile.txt" is the name of the input file.
'''

#check if filename included
if len(sys.argv) < 2:
	print "\nSYNTAX ERROR:"
	print "\tPlease include the input file as a command-line argument."
	print "\ti.e. 'python", sys.argv[0], "puzzlefile.txt'"
	print "\twhere 'puzzlefile.txt' is the name of the input file.\n"
	sys.exit()

#check if file exists
if os.path.isfile(sys.argv[1]):
	f = open(sys.argv[1], 'r')
	s = f.read()
else:
	s = "\nFILE ERROR:\n\t'" + sys.argv[1] 
	s += "' is not a file, or does not exist."
	print s
	sys.exit()


'''
	Formatting the Puzzle:
		blank tiles can be represented with 0 . * ?
		filled tiles are represented with [1-9]
		Puzzle encodings can have arbirary whitespace and newlines.
		
		Consider CNF Formula
		There are 9 values, 9 columns, and 9 rows, so 9*9*9=729 variables
		Then there are the clauses.
		For the minimal encoding we have 4 constraints:
			At least one number in each tile
			Each number appears at most once in each row
			Each number appears at most once in each col.
			Each number appears at most once in each 3x3 subgrid
'''


string_out = "p cnf "
v = 0
clause_counter = 0
CLAUSES = []

L = []
B = [] #boolean values for each variable in L.
#Consider T(i,j,k) to be a variable (of the 729 we need) where 0 < i,j,k < 10
#number k in cell (i,j)


i = 1
while i < 10:
	j = 1
	while j < 10:
		k = 1
		while k < 10:
			L.append([i,j,k])	#list of variables
			B.append(0)
			v += 1			#number of variables
			k += 1
		j += 1
	i += 1

#clauses

#unit clauses
col = 1
row = 1
for c in s:
	if c == '0' or c == '?' or c == '*' or c == '.':
		col += 1
		if col == 10:
			col = 1
			row += 1
	if c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' \
	   or c == '7' or c == '8' or c == '9':
		CLAUSES.append(formulas.unitClause(row, col, int(c)))
		clause_counter += 1
		col += 1
		if col == 10:
			col = 1
			row += 1

#one number in each tile
row = 1
col = 1
while row < 10:
	col = 1
	while col < 10:
		CLAUSES.append(formulas.ninearyClause(row, col))
		clause_counter += 1
		col += 1
	row += 1	

#these last three each produce 2916 clauses
#the first 2 are quite similar

#each number occurs at most once in each row
tL = []
row = 1
while row < 10:
	col = 1
	while col < 10:
		num = 1
		while num < 10:
			#write a clause for each other tile in the row (8)
			tL = formulas.rowClause(row, col, num)
			CLAUSES = CLAUSES + tL
			clause_counter += len(tL)
			num += 1
		col += 1
	row += 1


#each number occurs at most once in each column
tL = []
col = 1
while col < 10:
	row = 1
	while row < 10:
		num = 1
		while num < 10:
			#write a clause for each other tile in the column (8)
			tL = formulas.colClause(row, col, num)
			CLAUSES = CLAUSES + tL
			clause_counter += len(tL)
			num += 1
		row += 1
	col += 1


#each number occurs at most once in each 3x3 grid
tL = []
I = [[1,1], [4,1], [7,1], [1,4], [4,4], [7,4], [1,7], [4,7], [7,7]]
for p in I:
	r = 0
	while r < 3:
		q = 0
		while q < 3:
			num = 1
			while num < 10:
				tL = formulas.boxClause(p[0]+r, p[1]+q, num, p)
				CLAUSES = CLAUSES + tL
				clause_counter += len(tL)
				num += 1
			q += 1
		r += 1

string_out += str(v) + " " + str(clause_counter)
for mr_T in CLAUSES:
	string_out += "\n" + mr_T

print string_out



