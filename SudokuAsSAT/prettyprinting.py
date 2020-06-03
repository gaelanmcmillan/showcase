import sys
import os.path #for checking file existence
import re

#check if filename included
if len(sys.argv) < 2:
	print "\nSYNTAX ERROR:"
	print "\tPlease include the input file as a command-line argument."
	print "\ti.e. 'python", sys.argv[0], "SAT_out.txt'"
	print "\twhere 'SAT_out.txt' is the output of the satisfied SAT program.\n"
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

print s

P = []

for p in s:
	if p == "S":
		j = p+1
		while j < 8:
			P[j] = s[j]
			j += 1

		print P
