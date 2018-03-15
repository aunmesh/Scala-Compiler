class Node:
	def __init__(self, name, children=None):
		self.name = name
		if children:
              self.children = children
         else:
              self.children = [ ]

# Look into create leaf function if problems occur

def p_program_start(p):
	'''ProgramStart : ProgramStart class_objects
					| class_objects '''
	if(len(p) == 2):
		p[0] = Node("ProgramStart", [p[1]])
	else:
		p[0] = Node("ProgramStart", [p[1], p[2]])

# todo class_objects 

def p_class_objects(p):



# Block defination

def p_block(p):
	'''block : PARALCURLY block_statements_opt PARARCURLY'''
	leaf1 = Node("PARALCURLY")     #check if p[1] value i.e leaf value is required anywhere
	leaf2 = Node("PARARCURLY")
	p[0] = Node("block", [leaf1, p[1], leaf2])


def p_block_statements_opt(p):
	'''block_statements_opt : block_statements
							| empty '''
	p[0] = Node("block_statements_opt", [p[1]])

def p_block_statements(p):
	'''block_statements : block_statement
						| block_statements block_statement'''
	if (len(p) == 1):
		p[0] = Node("block_statements", [p[1]])
	else:
		p[0] = Node("block_statements", [p[1], p[2]])


# check grammar for this
def p_block_statement(p):
	'''block_statement : local_variable_declaration_statement 
					   | statement
					   | class_declaration
					   | SingletonObject
					   | method_declaration'''

	p[0] = Node("block_statement", [p[1]])

#end of block definitions

def p_SimpleLiteral(p):
	'''SimpleLiteral : ['-']INTEGER_LITS
					 | '''







def empty(p):
	'''empty : '''
	p[0] = Node("empty")
