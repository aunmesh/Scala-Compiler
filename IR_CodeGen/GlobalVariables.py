# All global variables associated with the code generator are stored here.

'''
Class Quadruple contains 3AC in list of list data structure
self.data[lineNo][0] contains block number
self.data[lineNo][1] contains line number
'''

class Quadruple(object):

	def __init__(self):
		self.data = []
		self.numblocks = 0

	'''
	load3AC - 3AC is loaded into Quadruple object
	Args:
		filename - file where the 3AC is stored
	
	Returns/Modifies:
		self.data - this is where the 3AC is stored
	'''

	def load3AC(self, filename):
		f = open(filename, 'r')
		i = 1
		self.data.append([])       # empty list added at the beginning to keep list index and line numbers consistent
		for line in f:
			self.data.append([0])
			currLine = line.split()
			self.data[i] = self.data[i] + currLine
			i += 1


	'''
	assignBlocks - Assigns Block Numbers to every 3AC line
	Args:
		none
	Returns/Modifies:
		self.data[lineNo][0] - this is where block number is assigned

	'''

	def assignBlocks(self):
		size = len(self.data)
		block = []   # temporary list to store information about leaders in 3AC
		for i in range(0,size):
			block.append(0)       
		
		# Assign 1 to all leaders in 3AC 	
		for i in range(1,size):
			if(self.data[i][2] == 'label'):
				block[i] = 1
			else:
				if (self.data[i][2] == 'call' or self.data[i][2] == 'ret'):
					if(i+1 <= size-1):
						block[i+1] = 1
				else:
					if (self.data[i][2] == 'goto' or self.data[i][2] == 'ifgoto'):
						if(i+1 <= size-1):
							block[i+1] = 1
							block[int(self.data[i][3])] = 1
		
		block[1] = 1  # First instruction is a leader

		for i in range(1,size):
			if (block[i] == 1):
				self.numblocks += 1

			self.data[i][0] = self.numblocks
