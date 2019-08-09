#converting to decimal
#formula from pdf: (i,j,k)--> 81(i-1) + 9(j-1) + (k-1) + 1
def cf(a,b,c):
	return 81*(a-1) + 9*(b-1) + (c-1) + 1



#Building the clauses is tricky. I'll write a function for each

def unitClause(row, column, number):
	return str(cf(row, column, number)) + " 0"

#each tile has a number
def ninearyClause(row, col):
	s = ''
	k = 1
	while k < 10:
		s += str(cf(row, col, k)) + " "
		k += 1
	s += '0'
	return s

#at most one of each number in each row
def rowClause(r,c,n):
	L = []
	col = c
	while col < 10:
		if col != c:
			L.append("-" + str(cf(r,c,n)) + " -" + str(cf(r, col, n)) + " 0")
		col += 1
	return L

#" column
def colClause(r,c,n):
	L = []
	row = r
	while row < 10:
		if row != r:
			L.append("-" + str(cf(r,c,n)) + " -" + str(cf(row,c,n)) + " 0")
		row += 1
	return L

#" 3x3 grid
def boxClause(r,c,n,p):
	L = []
	ths = [r,c]
	while ths[1] < p[1]+3:
		while ths[0] < p[0]+3:
			if ths != [r,c]:
				L.append("-" + str(cf(r,c,n)) + " -" + str(cf(ths[0],ths[1],n)) + " 0")
			ths[0] += 1
		ths[0] = p[0]
		ths[1] += 1
	return L




