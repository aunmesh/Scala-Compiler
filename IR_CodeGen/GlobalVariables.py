# All global variables associated with the code generator are stored here.

class Quadruple(object):

	def __init__(self):
		self.data = []

	def load3AC(self, filename):
		f = open(filename, 'r')
		i = 0
		for line in f:
			self.data.append([1])
			currLine = line.split()
			self.data[i] = self.data[i] + currLine
			i++