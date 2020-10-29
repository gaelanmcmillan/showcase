<<<<<<< HEAD
'''
NAME: chesschecker.py
AUTHOR: Andrew Meijer V00805554
PURPOSE: To verify whether or not a recorded chess game is valid. The chess game is valid if all of the recorded moves are legal chess moves.
DATE: Fall 2018, due Dec. 4, 2018.

INFORMATION ABOUT THE SOLUTION:
To implement a solution for the chess verification problem using concurrency, my original idea was to have some threads reading ahead in the move sequence to verify moves out of order. However, this caused problems and it did not provide much benefit compared to a linear single-threaded solution.
NEW APPROACH:
My new approach goes through all of the moves in order, and use three concurrent threads to verify each move. For each move, one thread ignores all other pieces on the board and checks if the move is a legal chess move according to how the piece is allowed to move. Another thread checks if there are other pieces blocking the move. A third thread checks if the move breaks any rules of check and checkmate. If all of these threads successfully verify the move, it is valid.
This program also uses a start thread to initialize variables and take input. The three concurrent threads use a barrier to make sure they are all working on the same move at the same time.
DATA STRUCTURE:
The data structure for this problem stores a position on the chess board. To store this, I use a 64 element list, one for each square on the board, a white piece is represented by a capital letter (P,N,B,R,Q,K) and a black piece is represented by a lowercase letter (p,n,b,r,q,k). An empty space is represented by a zero. The order of elements in the list goes in order: a1,b1,...,a2,b2,...,a8,...,g8,h8.
'''

#!/usr/bin/python3
import threading
import time
import re

# Global Variables
movelist = []
movingPiece = ''
winner = "nobody"
im = ""


#flags
fail = 0 		#game is invalid
done = 0 		#program is finished
inputdone = 0   #input is finished

#castling flags
WKmoved = 0
BKmoved = 0
A1moved = 0
H1moved = 0
A8moved = 0
H8moved = 0

#king check variables
wkingID = 0
bkingID = 0

#One Barrier is for white's move and one Barrier is for black's move.
#Threads synchronize to update the board every move.
wm_barrier = threading.Barrier(2)
bm_barrier = threading.Barrier(2)

#protected states
newList = [] 	#used by movethread / protected by barrier.
boardstate = []
#---------------

#movement functions
# these functions are used by the move thread for both black and white pieces
# they return a list of possible squares where a piece could be.
# pawn moves are handled separately
def KnightMove(rank, file, index):
	plist = []
	# only include squares that are on the 8x8 board.
	diff = 0
	if(file == 0):
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 1):
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 7):
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 6):
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	else:
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index-diff)

	return plist		
	
def BishopMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# only include squares that are on the board.
	if(file != 0):
		diff = 7
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 7
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -9
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 9
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
			
	if(file != 7):
		diff = 9
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 9
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -7
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 7
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	

	return plist
	
def RookMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# update A1/H1 moved here OR
	# update in the spaceThread .
	
	# vertical movement along files
	diff = 8
	while(index+diff < 64):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = 64 # break
		diff = diff + 8
	diff = -8
	while(index+diff > -1):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = -100 # break
		diff = diff - 8
		
	# horizontal movement along ranks
	diff = 1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff + 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)	
	diff = -1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff - 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)
	
	return plist
	
def QueenMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# only include squares that are on the board.
	if(file != 0):
		diff = 7
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 7
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -9
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 9
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
			
	if(file != 7):
		diff = 9
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 9
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -7
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 7
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
				
	# vertical movement along files
	diff = 8
	while(index+diff < 64):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = 64 # break
		diff = diff + 8
	diff = -8
	while(index+diff > -1):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = -100 # break
		diff = diff - 8
		
	# horizontal movement along ranks
	diff = 1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff + 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)	
	diff = -1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff - 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)
	
	return plist
	
def KingMove(rank, file, index):
	plist = []
	# only include squares that are on the 8x8 board.
	diff = 0
	if(file == 0):
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 9
		if(index+diff < 64):
			plist.append(index+diff)
		diff = 1
		plist.append(index+diff)
		diff = -7
		if(index+diff > -1):
			plist.append(index+diff)
	elif(file == 7):
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 7
		if(index+diff < 64):
			plist.append(index+diff)
		diff = -1
		plist.append(index+diff)
		diff = -9
		if(index+diff > -1):
			plist.append(index+diff)
	else:
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 9
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 7
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 1
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)

	return plist
	
	
#more functions

#return the set of elements that are in both lists
def findIntersection(list1, list2):
	list = []
	
	if(len(list1) is not 0 and len(list2) is not 0):
		for x in list1:
			for y in list2:
				if (x == y):
					list.append(x)
	elif(len(list1) is not 0):
		list = list1
	else:
		list = list2
	
	sh_list = []

	for n in list:
		if(movingPiece is boardstate[n]):
			sh_list.append(n)

	
	return sh_list
	

#return boardstate indicies for a certain column or row
def findIndicies(rc):
	#the id could be a rank or a column
	ids = []
	if(rc is 'a'):
		ids = [0,8,16,24,32,40,48,56]
		return ids
	elif(rc is 'b'):
		ids = [1,9,17,25,33,41,49,57]
		return ids
	elif(rc is 'c'):
		ids = [2,10,18,26,34,42,50,58]
		return ids
	elif(rc is 'd'):
		ids = [3,11,19,27,35,43,51,59]
		return ids
	elif(rc is 'e'):
		ids = [4,12,20,28,36,44,52,60]
		return ids
	elif(rc is 'f'):
		ids = [5,13,21,29,37,45,53,61]
		return ids
	elif(rc is 'g'):
		ids = [6,14,22,30,38,46,54,62]
		return ids
	elif(rc is 'h'):
		ids = [7,15,23,31,39,47,55,63]
		return ids
	elif(rc == 1):
		ids = [0,1,2,3,4,5,6,7]
		return ids
	elif(rc == 2):
		ids = [8,9,10,11,12,13,14,15]
		return ids
	elif(rc == 3):
		ids = [16,17,18,19,20,21,22,23]
		return ids
	elif(rc == 4):
		ids = [24,25,26,27,28,29,30,31]
		return ids
	elif(rc == 5):
		ids = [32,33,34,35,36,37,38,39]
		return ids
	elif(rc == 6):
		ids = [40,41,42,43,44,45,46,47]
		return ids
	elif(rc == 7):
		ids = [48,49,50,51,52,53,54,55]
		return ids
	elif(rc == 8):
		ids = [56,57,58,59,60,61,62,63]
		return ids														
	else:
		ids = []
		return ids
		

class startThread(threading.Thread):
	def run(self):
		print ("Welcome to chess. Please be careful of syntax.")
		global inputdone
		
		m = input("Please enter the name of the text file with the chess game you would like to verify, or just press Enter to proceed with the default file 'samplegame.txt':")

		if(m == ""):
			fileobject = open("samplegame.txt","r")
		else:
			fileobject = open(m,"r")
		
		#read movelist from file
		stro = fileobject.read()
		fileobject.close()
		
		if(stro == ""):
			print("Input Error.")
		
		#store the input
		global movelist
		movelist = stro.split('\n')
		
		#set starting boardstate
		global boardstate
		boardstate = ['R','N','B','Q','K','B','N','R','P','P','P','P','P','P','P','P','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','p','p','p','p','p','p','p','p','r','n','b','q','k','b','n','r']
		
		inputdone = 1

#checks if the move is valid ignoring the other pieces on the board.
#moveThread also checks for "0-1" and "1-0"
class moveThread(threading.Thread):
	def run(self):
		global im
		global winner
		global fail
		global done
		global movelist
		global movingPiece
		global H1moved
		global A1moved
		global A8moved
		global H8moved
		global WKmoved
		global BKmoved
		global newList
		currentmove = 0
		#synchronized start:
		wm_barrier.wait()
		wm_barrier.reset()
		for m in movelist:
			
			if(done == 0):
				currentmove += 1

				if(" " not in m):
					if(m == "0-1\n" or m == "0-1"):
						winner = "black"
						done = 1
					elif(m == "1-0\n" or m == "1-0"):
						winner = "white"
						done = 1
					else:
						im = m
						fail = 1
						done = 1
				else:	
					wm,bm = m.split(" ")
					if(len(wm) < 2):
						im = wm
						fail = 1
						done = 1
					elif(wm == "O-O-O"):
						#queenside castle
						if (A1moved or WKmoved):
							im = wm
							fail = 1
							done = 1
						#queenside castle
						if(boardstate[1] is not '0' or boardstate[2] is not '0' or boardstate[3] is not '0'):
							# No space
							im = wm
							fail = 1
							done = 1
					elif(wm == "O-O"):
						#kingside castle
						if (H1moved or WKmoved):
							im = wm
							fail = 1
							done = 1
						#kingside castle
						if(boardstate[5] is not '0' or boardstate[6] is not '0'):
							# No space
							im = wm
							fail = 1
							done = 1
					elif(wm == "0-1"):
						winner = "black"
						done = 1
					elif(wm == "1-0"): 
						winner = "white"
						done = 1
					else:
						# in this branch,I know the format of the move , maximum 6 characters:
						# [primary id][secondary id][captures?][file][rank][check/checkmate]
						# I use a regular expression to remove 'captures' and 'check/checkmate' characters.
						wm = re.sub(r'[x]|[^\w]', '', wm)
						
						rank = int(wm[len(wm)-1])
						if(wm[len(wm)-2] is 'a'):
							file = 0
						elif(wm[len(wm)-2] is 'b'):
							file = 1
						elif(wm[len(wm)-2] is 'c'):
							file = 2
						elif(wm[len(wm)-2] is 'd'):
							file = 3
						elif(wm[len(wm)-2] is 'e'):
							file = 4
						elif(wm[len(wm)-2] is 'f'):
							file = 5
						elif(wm[len(wm)-2] is 'g'):
							file = 6
						elif(wm[len(wm)-2] is 'h'):
							file = 7
						else:
							im = wm
							fail = 1
							done = 1
						
						#determine the index of the boardstate
						index = file + (8*(rank-1))
						
						# do not capture your own piece
						if(boardstate[index] in ['P','N','B','R','Q','K']):
							im = wm
							fail = 1
							done = 1
						
						#sidlist gives a list of the squares identified by the secondary ID.
						sidlist = []
						if(len(wm) == 4):
							sidlist = findIndicies(wm[1])
							if(sidlist is []):
								im = wm
								fail = 1
								done = 1
								
						#plist gives a list of the possible candidate squares where the piece could be.
						plist = []
						if(wm[0] is 'N'):
							movingPiece = 'N'
							plist = KnightMove(rank, file, index)
							
						elif(wm[0] is 'B'):
							movingPiece = 'B'
							plist = BishopMove(rank, file, index)
						elif(wm[0] is 'R'):				
							movingPiece = 'R'
							plist = RookMove(rank, file, index)
							
						elif(wm[0] is 'Q'):
							movingPiece = 'Q'
							plist = QueenMove(rank, file, index)
							
						elif(wm[0] is 'K'):
							movingPiece = 'K'
							WKmoved = 1
							plist = KingMove(rank, file, index)
							
						else:
							#pawn move
							#does not yet account for double-moves.
							movingPiece = 'P'
							fromrank = int(wm[len(wm)-1]) - 1
							
							# perform fromrank++ iff pawn is moving 2 square
							plist = findIndicies(fromrank)
							sidlist = findIndicies(wm[0])
							if(sidlist is []):
								im = wm
								fail = 1
								done = 1
							possiblepawn = findIntersection(sidlist, plist)

							if(len(possiblepawn) != 1):
								fromrank = fromrank-1
								plist = findIndicies(fromrank)
					
										
						#plist and sidmist are used to determine which piece is being moved.
						#sometimes it cannot be determined without knowing the boardstate.

						newList = findIntersection(sidlist, plist)

						# error checking not included here for moves where multiple pieces of the same type are 	candidates, but one of them is blocked by a piece.
						# For now, if there are multiple candidates, then throw error.								
			wm_barrier.wait()
			if(done == 0):
				if(len(newList) != 1):
					im = wm
					fail = 1
					done = 1
				else:
					#update board
					if(newList[0] > 63 or newList[0] < 0):
						im=wm
						fail=1
						done=1
					elif(wm == "O-O-O"):
						boardstate[0] = '0'
						boardstate[1] = '0'
						boardstate[2] = 'K'
						boardstate[3] = 'R'
						boardstate[4] = '0'
						print("Board Updated for white: queenside castle.")
					elif(wm == "O-O"):
						boardstate[4] = '0'
						boardstate[5] = 'R'
						boardstate[6] = 'K'
						boardstate[7] = '0'
						print("Board Updated for white: kingside castle.")
					else:
						boardstate[index] = boardstate[newList[0]]
						boardstate[newList[0]] = '0'
						print("Board Updated for white: piece from ",newList[0] , " moved to ", index ,".")
					
			wm_barrier.reset()
			
			if(done == 0):
				#black's move
				if(len(bm) < 2):
					im = bm
					fail = 1
					done = 1
				
				if(bm == "O-O-O"):
					#queenside castle
					if (A8moved or BKmoved):
						im = bm
						fail = 1
						done = 1
					if(boardstate[57] is not '0' or boardstate[58] is not '0' or boardstate[59] is not '0'):
						# No space
						im = bm
						fail = 1
						done = 1	
				elif(bm == "O-O"):
					#kingside castle
					if (H8moved or BKmoved):
						im = bm
						fail = 1
						done = 1
					if(boardstate[61] is not '0' or boardstate[62] is not '0'):
						# No space
						im = bm
						fail = 1
						done = 1
				elif(bm == "0-1"):
					winner = "black"
					done = 1
				elif(bm == "1-0"): 
					winner = "white"
					done = 1
				else:
					# in this branch,I know the format of the move , maximum 6 characters:
					# [primary id][secondary id][captures?][file][rank][check/checkmate]
					# I use a regular expression to remove 'captures' and 'check/checkmate' characters.
					bm = re.sub(r'[x]|[^\w]', '', bm)
					
					rank = int(bm[len(bm)-1])
					if(bm[len(bm)-2] is 'a'):
						file = 0
					elif(bm[len(bm)-2] is 'b'):
						file = 1
					elif(bm[len(bm)-2] is 'c'):
						file = 2
					elif(bm[len(bm)-2] is 'd'):
						file = 3
					elif(bm[len(bm)-2] is 'e'):
						file = 4
					elif(bm[len(bm)-2] is 'f'):
						file = 5
					elif(bm[len(bm)-2] is 'g'):
						file = 6
					elif(bm[len(bm)-2] is 'h'):
						file = 7
					else:
						im = bm
						fail = 1
						done = 1
						
					#determine the index of the boardstate
					index = file + (8*(rank-1))
					
					# do not capture your own pieces
					if(boardstate[index] in ['p','n','b','r','q','k']):
						im = bm
						fail = 1
						done = 1
						
					#sidlist gives a list of the squares identified by the secondary ID.
					sidlist = []
					if(len(bm) == 4):
						sidlist = findIndicies(bm[1])
						if(sidlist is []):
							im = bm
							fail = 1
							done = 1
										
					#plist gives a list of the possible candidate squares where the piece could be.
					plist = []
					if(bm[0] is 'N'):
						movingPiece = 'n'
						plist = KnightMove(rank, file, index)
						
					elif(bm[0] is 'B'):
						movingPiece = 'b'
						plist = BishopMove(rank, file, index)
					elif(bm[0] is 'R'):				
						movingPiece = 'r'
						plist = RookMove(rank, file, index)
						
					elif(bm[0] is 'Q'):
						movingPiece = 'q'
						plist = QueenMove(rank, file, index)
					elif(bm[0] is 'K'):
						movingPiece = 'k'
						BKmoved = 1
						plist = KingMove(rank, file, index)
						
					else:
						#pawn move
						movingPiece = 'p'
						fromrank = int(bm[len(bm)-1]) + 1
						
						# perform fromrank-- iff pawn is moving 2 square
						plist = findIndicies(fromrank)
						
						sidlist = findIndicies(bm[0])
						if(sidlist is []):
							im = bm
							fail = 1
							done = 1
						
						possiblepawn = findIntersection(sidlist, plist)
						if(len(possiblepawn) != 1):
							fromrank = fromrank+1
							plist = findIndicies(fromrank)
						
					#plist and sidmist are used to determine which piece is being moved.
					#sometimes it cannot be determined in movethread.
					#spacethread will determine the locations of the pieces and make the moves.
					
					#if we get to this point with no whammies, the movethread has succeeded.
					newList = findIntersection(sidlist, plist)
			bm_barrier.wait()
			
			if(done == 0):
			
				if(len(newList) != 1):
					im = bm
					fail = 1
					done = 1
					
				else:
					#update board
					if(newList[0] > 63 or newList[0] < 0):
						im = bm
						fail=1
						done=1
		
					elif(bm == "O-O-O"):
						boardstate[56] = '0'
						boardstate[57] = '0'
						boardstate[58] = 'k'
						boardstate[59] = 'r'
						boardstate[60] = '0'
						print("Board Updated for black: queenside castle.")
					elif(bm == "O-O"):	
						boardstate[60] = '0'
						boardstate[61] = 'r'
						boardstate[62] = 'k'
						boardstate[63] = '0'
						print("Board Updated for black: kingside castle.")
					else:
						boardstate[index] = boardstate[newList[0]]
						boardstate[newList[0]] = '0'
						print("Board Updated for black: piece from ",newList[0] , " moved to ", index ,".")
			bm_barrier.reset()
	
#checks if the move respects the rules of check and checkmate
class checkThread(threading.Thread):
	def run(self):
		global im
		global fail
		global done
		global movelist
		currentmove = 0
		#synchronized start:
		wm_barrier.wait()
		for m in movelist:

			currentmove += 1
			

			wm_barrier.wait()
			
			# black move
			bm_barrier.wait()
		done = 1
		
	
# MAIN #
# Create new threads
t1 = startThread()
t2 = moveThread()
t3 = checkThread()
# Threads can only be started once
t1.start()
# wait for input to finish
while(inputdone == 0):
	pass

print("Input Successful.")
t1.join()

t2.start()
t3.start()

while(done == 0):
	pass

t2.join()
t3.join()
	
if(fail == 0):
	print("Valid game.")
	print(winner, "is victorious.")
else:
	print("Invalid game.")
	print("error: ", im)


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
=======
'''
NAME: chesschecker.py
AUTHOR: Andrew Meijer V00805554
PURPOSE: To verify whether or not a recorded chess game is valid. The chess game is valid if all of the recorded moves are legal chess moves.
DATE: Fall 2018, due Dec. 4, 2018.

INFORMATION ABOUT THE SOLUTION:
To implement a solution for the chess verification problem using concurrency, my original idea was to have some threads reading ahead in the move sequence to verify moves out of order. However, this caused problems and it did not provide much benefit compared to a linear single-threaded solution.
NEW APPROACH:
My new approach goes through all of the moves in order, and use three concurrent threads to verify each move. For each move, one thread ignores all other pieces on the board and checks if the move is a legal chess move according to how the piece is allowed to move. Another thread checks if there are other pieces blocking the move. A third thread checks if the move breaks any rules of check and checkmate. If all of these threads successfully verify the move, it is valid.
This program also uses a start thread to initialize variables and take input. The three concurrent threads use a barrier to make sure they are all working on the same move at the same time.
DATA STRUCTURE:
The data structure for this problem stores a position on the chess board. To store this, I use a 64 element list, one for each square on the board, a white piece is represented by a capital letter (P,N,B,R,Q,K) and a black piece is represented by a lowercase letter (p,n,b,r,q,k). An empty space is represented by a zero. The order of elements in the list goes in order: a1,b1,...,a2,b2,...,a8,...,g8,h8.
'''

#!/usr/bin/python3
import threading
import time
import re

# Global Variables
movelist = []
movingPiece = ''
winner = "nobody"
im = ""


#flags
fail = 0 		#game is invalid
done = 0 		#program is finished
inputdone = 0   #input is finished

#castling flags
WKmoved = 0
BKmoved = 0
A1moved = 0
H1moved = 0
A8moved = 0
H8moved = 0

#king check variables
wkingID = 0
bkingID = 0

#One Barrier is for white's move and one Barrier is for black's move.
#Threads synchronize to update the board every move.
wm_barrier = threading.Barrier(2)
bm_barrier = threading.Barrier(2)

#protected states
newList = [] 	#used by movethread / protected by barrier.
boardstate = []
#---------------

#movement functions
# these functions are used by the move thread for both black and white pieces
# they return a list of possible squares where a piece could be.
# pawn moves are handled separately
def KnightMove(rank, file, index):
	plist = []
	# only include squares that are on the 8x8 board.
	diff = 0
	if(file == 0):
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 1):
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 7):
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	elif(file == 6):
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
	else:
		diff = 6
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 10
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 15
		if(index+diff < 64):
			plist.append(index+diff)
		if(index-diff > -1):
			plist.append(index-diff)
		diff = 17
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index-diff)

	return plist		
	
def BishopMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# only include squares that are on the board.
	if(file != 0):
		diff = 7
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 7
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -9
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 9
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
			
	if(file != 7):
		diff = 9
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 9
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -7
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 7
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	

	return plist
	
def RookMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# update A1/H1 moved here OR
	# update in the spaceThread .
	
	# vertical movement along files
	diff = 8
	while(index+diff < 64):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = 64 # break
		diff = diff + 8
	diff = -8
	while(index+diff > -1):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = -100 # break
		diff = diff - 8
		
	# horizontal movement along ranks
	diff = 1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff + 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)	
	diff = -1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff - 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)
	
	return plist
	
def QueenMove(rank, file, index):
	plist = []
	edge = [0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
	# only include squares that are on the board.
	if(file != 0):
		diff = 7
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 7
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -9
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 9
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
			
	if(file != 7):
		diff = 9
		while(index+diff < 64 and index+diff not in edge):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff + 9
		if(index+diff < 64):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)	
		
		diff = -7
		while(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
			else:
				break
			diff = diff - 7
		if(index+diff > -1):
			if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
				plist.append(index+diff)
				
	# vertical movement along files
	diff = 8
	while(index+diff < 64):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = 64 # break
		diff = diff + 8
	diff = -8
	while(index+diff > -1):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			diff = -100 # break
		diff = diff - 8
		
	# horizontal movement along ranks
	diff = 1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff + 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)	
	diff = -1
	while(index+diff not in edge):
		if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
			plist.append(index+diff)
		else:
			break
		diff = diff - 1
	if(boardstate[index+diff] is movingPiece or boardstate[index+diff] is '0'):
		plist.append(index+diff)
	
	return plist
	
def KingMove(rank, file, index):
	plist = []
	# only include squares that are on the 8x8 board.
	diff = 0
	if(file == 0):
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 9
		if(index+diff < 64):
			plist.append(index+diff)
		diff = 1
		plist.append(index+diff)
		diff = -7
		if(index+diff > -1):
			plist.append(index+diff)
	elif(file == 7):
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 7
		if(index+diff < 64):
			plist.append(index+diff)
		diff = -1
		plist.append(index+diff)
		diff = -9
		if(index+diff > -1):
			plist.append(index+diff)
	else:
		diff = 8
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 9
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 7
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)
		diff = 1
		if(index+diff < 64):
			plist.append(index+diff)
		if(index+diff > -1):
			plist.append(index+diff)

	return plist
	
	
#more functions

#return the set of elements that are in both lists
def findIntersection(list1, list2):
	list = []
	
	if(len(list1) is not 0 and len(list2) is not 0):
		for x in list1:
			for y in list2:
				if (x == y):
					list.append(x)
	elif(len(list1) is not 0):
		list = list1
	else:
		list = list2
	
	sh_list = []

	for n in list:
		if(movingPiece is boardstate[n]):
			sh_list.append(n)

	
	return sh_list
	

#return boardstate indicies for a certain column or row
def findIndicies(rc):
	#the id could be a rank or a column
	ids = []
	if(rc is 'a'):
		ids = [0,8,16,24,32,40,48,56]
		return ids
	elif(rc is 'b'):
		ids = [1,9,17,25,33,41,49,57]
		return ids
	elif(rc is 'c'):
		ids = [2,10,18,26,34,42,50,58]
		return ids
	elif(rc is 'd'):
		ids = [3,11,19,27,35,43,51,59]
		return ids
	elif(rc is 'e'):
		ids = [4,12,20,28,36,44,52,60]
		return ids
	elif(rc is 'f'):
		ids = [5,13,21,29,37,45,53,61]
		return ids
	elif(rc is 'g'):
		ids = [6,14,22,30,38,46,54,62]
		return ids
	elif(rc is 'h'):
		ids = [7,15,23,31,39,47,55,63]
		return ids
	elif(rc == 1):
		ids = [0,1,2,3,4,5,6,7]
		return ids
	elif(rc == 2):
		ids = [8,9,10,11,12,13,14,15]
		return ids
	elif(rc == 3):
		ids = [16,17,18,19,20,21,22,23]
		return ids
	elif(rc == 4):
		ids = [24,25,26,27,28,29,30,31]
		return ids
	elif(rc == 5):
		ids = [32,33,34,35,36,37,38,39]
		return ids
	elif(rc == 6):
		ids = [40,41,42,43,44,45,46,47]
		return ids
	elif(rc == 7):
		ids = [48,49,50,51,52,53,54,55]
		return ids
	elif(rc == 8):
		ids = [56,57,58,59,60,61,62,63]
		return ids														
	else:
		ids = []
		return ids
		

class startThread(threading.Thread):
	def run(self):
		print ("Welcome to chess. Please be careful of syntax.")
		global inputdone
		
		m = input("Please enter the name of the text file with the chess game you would like to verify, or just press Enter to proceed with the default file 'samplegame.txt':")

		if(m == ""):
			fileobject = open("samplegame.txt","r")
		else:
			fileobject = open(m,"r")
		
		#read movelist from file
		stro = fileobject.read()
		fileobject.close()
		
		if(stro == ""):
			print("Input Error.")
		
		#store the input
		global movelist
		movelist = stro.split('\n')
		
		#set starting boardstate
		global boardstate
		boardstate = ['R','N','B','Q','K','B','N','R','P','P','P','P','P','P','P','P','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','p','p','p','p','p','p','p','p','r','n','b','q','k','b','n','r']
		
		inputdone = 1

#checks if the move is valid ignoring the other pieces on the board.
#moveThread also checks for "0-1" and "1-0"
class moveThread(threading.Thread):
	def run(self):
		global im
		global winner
		global fail
		global done
		global movelist
		global movingPiece
		global H1moved
		global A1moved
		global A8moved
		global H8moved
		global WKmoved
		global BKmoved
		global newList
		currentmove = 0
		#synchronized start:
		wm_barrier.wait()
		wm_barrier.reset()
		for m in movelist:
			
			if(done == 0):
				currentmove += 1

				if(" " not in m):
					if(m == "0-1\n" or m == "0-1"):
						winner = "black"
						done = 1
					elif(m == "1-0\n" or m == "1-0"):
						winner = "white"
						done = 1
					else:
						im = m
						fail = 1
						done = 1
				else:	
					wm,bm = m.split(" ")
					if(len(wm) < 2):
						im = wm
						fail = 1
						done = 1
					elif(wm == "O-O-O"):
						#queenside castle
						if (A1moved or WKmoved):
							im = wm
							fail = 1
							done = 1
						#queenside castle
						if(boardstate[1] is not '0' or boardstate[2] is not '0' or boardstate[3] is not '0'):
							# No space
							im = wm
							fail = 1
							done = 1
					elif(wm == "O-O"):
						#kingside castle
						if (H1moved or WKmoved):
							im = wm
							fail = 1
							done = 1
						#kingside castle
						if(boardstate[5] is not '0' or boardstate[6] is not '0'):
							# No space
							im = wm
							fail = 1
							done = 1
					elif(wm == "0-1"):
						winner = "black"
						done = 1
					elif(wm == "1-0"): 
						winner = "white"
						done = 1
					else:
						# in this branch,I know the format of the move , maximum 6 characters:
						# [primary id][secondary id][captures?][file][rank][check/checkmate]
						# I use a regular expression to remove 'captures' and 'check/checkmate' characters.
						wm = re.sub(r'[x]|[^\w]', '', wm)
						
						rank = int(wm[len(wm)-1])
						if(wm[len(wm)-2] is 'a'):
							file = 0
						elif(wm[len(wm)-2] is 'b'):
							file = 1
						elif(wm[len(wm)-2] is 'c'):
							file = 2
						elif(wm[len(wm)-2] is 'd'):
							file = 3
						elif(wm[len(wm)-2] is 'e'):
							file = 4
						elif(wm[len(wm)-2] is 'f'):
							file = 5
						elif(wm[len(wm)-2] is 'g'):
							file = 6
						elif(wm[len(wm)-2] is 'h'):
							file = 7
						else:
							im = wm
							fail = 1
							done = 1
						
						#determine the index of the boardstate
						index = file + (8*(rank-1))
						
						# do not capture your own piece
						if(boardstate[index] in ['P','N','B','R','Q','K']):
							im = wm
							fail = 1
							done = 1
						
						#sidlist gives a list of the squares identified by the secondary ID.
						sidlist = []
						if(len(wm) == 4):
							sidlist = findIndicies(wm[1])
							if(sidlist is []):
								im = wm
								fail = 1
								done = 1
								
						#plist gives a list of the possible candidate squares where the piece could be.
						plist = []
						if(wm[0] is 'N'):
							movingPiece = 'N'
							plist = KnightMove(rank, file, index)
							
						elif(wm[0] is 'B'):
							movingPiece = 'B'
							plist = BishopMove(rank, file, index)
						elif(wm[0] is 'R'):				
							movingPiece = 'R'
							plist = RookMove(rank, file, index)
							
						elif(wm[0] is 'Q'):
							movingPiece = 'Q'
							plist = QueenMove(rank, file, index)
							
						elif(wm[0] is 'K'):
							movingPiece = 'K'
							WKmoved = 1
							plist = KingMove(rank, file, index)
							
						else:
							#pawn move
							#does not yet account for double-moves.
							movingPiece = 'P'
							fromrank = int(wm[len(wm)-1]) - 1
							
							# perform fromrank++ iff pawn is moving 2 square
							plist = findIndicies(fromrank)
							sidlist = findIndicies(wm[0])
							if(sidlist is []):
								im = wm
								fail = 1
								done = 1
							possiblepawn = findIntersection(sidlist, plist)

							if(len(possiblepawn) != 1):
								fromrank = fromrank-1
								plist = findIndicies(fromrank)
					
										
						#plist and sidmist are used to determine which piece is being moved.
						#sometimes it cannot be determined without knowing the boardstate.

						newList = findIntersection(sidlist, plist)

						# error checking not included here for moves where multiple pieces of the same type are 	candidates, but one of them is blocked by a piece.
						# For now, if there are multiple candidates, then throw error.								
			wm_barrier.wait()
			if(done == 0):
				if(len(newList) != 1):
					im = wm
					fail = 1
					done = 1
				else:
					#update board
					if(newList[0] > 63 or newList[0] < 0):
						im=wm
						fail=1
						done=1
					elif(wm == "O-O-O"):
						boardstate[0] = '0'
						boardstate[1] = '0'
						boardstate[2] = 'K'
						boardstate[3] = 'R'
						boardstate[4] = '0'
						print("Board Updated for white: queenside castle.")
					elif(wm == "O-O"):
						boardstate[4] = '0'
						boardstate[5] = 'R'
						boardstate[6] = 'K'
						boardstate[7] = '0'
						print("Board Updated for white: kingside castle.")
					else:
						boardstate[index] = boardstate[newList[0]]
						boardstate[newList[0]] = '0'
						print("Board Updated for white: piece from ",newList[0] , " moved to ", index ,".")
					
			wm_barrier.reset()
			
			if(done == 0):
				#black's move
				if(len(bm) < 2):
					im = bm
					fail = 1
					done = 1
				
				if(bm == "O-O-O"):
					#queenside castle
					if (A8moved or BKmoved):
						im = bm
						fail = 1
						done = 1
					if(boardstate[57] is not '0' or boardstate[58] is not '0' or boardstate[59] is not '0'):
						# No space
						im = bm
						fail = 1
						done = 1	
				elif(bm == "O-O"):
					#kingside castle
					if (H8moved or BKmoved):
						im = bm
						fail = 1
						done = 1
					if(boardstate[61] is not '0' or boardstate[62] is not '0'):
						# No space
						im = bm
						fail = 1
						done = 1
				elif(bm == "0-1"):
					winner = "black"
					done = 1
				elif(bm == "1-0"): 
					winner = "white"
					done = 1
				else:
					# in this branch,I know the format of the move , maximum 6 characters:
					# [primary id][secondary id][captures?][file][rank][check/checkmate]
					# I use a regular expression to remove 'captures' and 'check/checkmate' characters.
					bm = re.sub(r'[x]|[^\w]', '', bm)
					
					rank = int(bm[len(bm)-1])
					if(bm[len(bm)-2] is 'a'):
						file = 0
					elif(bm[len(bm)-2] is 'b'):
						file = 1
					elif(bm[len(bm)-2] is 'c'):
						file = 2
					elif(bm[len(bm)-2] is 'd'):
						file = 3
					elif(bm[len(bm)-2] is 'e'):
						file = 4
					elif(bm[len(bm)-2] is 'f'):
						file = 5
					elif(bm[len(bm)-2] is 'g'):
						file = 6
					elif(bm[len(bm)-2] is 'h'):
						file = 7
					else:
						im = bm
						fail = 1
						done = 1
						
					#determine the index of the boardstate
					index = file + (8*(rank-1))
					
					# do not capture your own pieces
					if(boardstate[index] in ['p','n','b','r','q','k']):
						im = bm
						fail = 1
						done = 1
						
					#sidlist gives a list of the squares identified by the secondary ID.
					sidlist = []
					if(len(bm) == 4):
						sidlist = findIndicies(bm[1])
						if(sidlist is []):
							im = bm
							fail = 1
							done = 1
										
					#plist gives a list of the possible candidate squares where the piece could be.
					plist = []
					if(bm[0] is 'N'):
						movingPiece = 'n'
						plist = KnightMove(rank, file, index)
						
					elif(bm[0] is 'B'):
						movingPiece = 'b'
						plist = BishopMove(rank, file, index)
					elif(bm[0] is 'R'):				
						movingPiece = 'r'
						plist = RookMove(rank, file, index)
						
					elif(bm[0] is 'Q'):
						movingPiece = 'q'
						plist = QueenMove(rank, file, index)
					elif(bm[0] is 'K'):
						movingPiece = 'k'
						BKmoved = 1
						plist = KingMove(rank, file, index)
						
					else:
						#pawn move
						movingPiece = 'p'
						fromrank = int(bm[len(bm)-1]) + 1
						
						# perform fromrank-- iff pawn is moving 2 square
						plist = findIndicies(fromrank)
						
						sidlist = findIndicies(bm[0])
						if(sidlist is []):
							im = bm
							fail = 1
							done = 1
						
						possiblepawn = findIntersection(sidlist, plist)
						if(len(possiblepawn) != 1):
							fromrank = fromrank+1
							plist = findIndicies(fromrank)
						
					#plist and sidmist are used to determine which piece is being moved.
					#sometimes it cannot be determined in movethread.
					#spacethread will determine the locations of the pieces and make the moves.
					
					#if we get to this point with no whammies, the movethread has succeeded.
					newList = findIntersection(sidlist, plist)
			bm_barrier.wait()
			
			if(done == 0):
			
				if(len(newList) != 1):
					im = bm
					fail = 1
					done = 1
					
				else:
					#update board
					if(newList[0] > 63 or newList[0] < 0):
						im = bm
						fail=1
						done=1
		
					elif(bm == "O-O-O"):
						boardstate[56] = '0'
						boardstate[57] = '0'
						boardstate[58] = 'k'
						boardstate[59] = 'r'
						boardstate[60] = '0'
						print("Board Updated for black: queenside castle.")
					elif(bm == "O-O"):	
						boardstate[60] = '0'
						boardstate[61] = 'r'
						boardstate[62] = 'k'
						boardstate[63] = '0'
						print("Board Updated for black: kingside castle.")
					else:
						boardstate[index] = boardstate[newList[0]]
						boardstate[newList[0]] = '0'
						print("Board Updated for black: piece from ",newList[0] , " moved to ", index ,".")
			bm_barrier.reset()
	
#checks if the move respects the rules of check and checkmate
class checkThread(threading.Thread):
	def run(self):
		global im
		global fail
		global done
		global movelist
		currentmove = 0
		#synchronized start:
		wm_barrier.wait()
		for m in movelist:

			currentmove += 1
			

			wm_barrier.wait()
			
			# black move
			bm_barrier.wait()
		done = 1
		
	
# MAIN #
# Create new threads
t1 = startThread()
t2 = moveThread()
t3 = checkThread()
# Threads can only be started once
t1.start()
# wait for input to finish
while(inputdone == 0):
	pass

print("Input Successful.")
t1.join()

t2.start()
t3.start()

while(done == 0):
	pass

t2.join()
t3.join()
	
if(fail == 0):
	print("Valid game.")
	print(winner, "is victorious.")
else:
	print("Invalid game.")
	print("error: ", im)


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
>>>>>>> b56fdf5242c84ded64b4ac42cc225a15012796a5
