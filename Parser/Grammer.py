Dict = {"KW_object"}

class Node:
	def __init__(self, name, children=None):
		self.name = name
		if children:
              self.children = children
         else:
              self.children = [ ]



def leaf_gen(name, val):
	leaf = Node(val)
	preleaf = Node(name, [leaf])
	return preleaf

# Look into create leaf function if problems occur

def p_program_start(p):
	'''ProgramStart : ProgramStart class_objects
					| class_objects '''
	if(len(p) == 2):
		p[0] = Node(Dict["ProgramStructure"], [p[1]])
	else:
		p[0] = Node(Dict["ProgramStructure"], [p[1], p[2]])

# todo class_objects 

def p_class_objects(p):
	'''class_objects : SingletonObject
						 | class_declaration'''
	p[0] = Node(Dict["class_and_objects"], [p[1]])

def p_SingletonObject(p):
	'''SingletonObject : ObjectDeclare block'''
	p[0] = Node(Dict["SingletonObject"], [p[1], p[2]])

def p_object_declare(p):
	'''ObjectDeclare : KW_object IDENTIFIER 
							| KW_object IDENTIFIER KW_extends IDENTIFIER'''
	if (len(p) == 5):
		leaf1 = leaf_gen(Dict["KEYWORD_OBJECT"], p[1])
		leaf2 = leaf_gen(Dict["IDENTIFIER"], p[2])
		leaf3 = leaf_gen(Dict["KEYWORD_EXTENDS"], p[3])
		leaf4 = leaf_gen(Dict["IDENTIFIER"], p[4])
		p[0] = Node(Dict["ObjectDeclare"], [leaf1, leaf2, leaf3, leaf4])
	else:
		leaf1 = leaf_gen(Dict["KEYWORD_OBJECT"], p[1])
		leaf2 = leaf_gen(Dict["IDENTIFIER"], p[2])
		p[0] = Node(Dict["ObjectDeclare"], [leaf1, leaf2])





# Block defination

def p_block(p):
	'''block : PARALCURLY block_statements_opt PARARCURLY'''
	leaf1 = leaf_gen(Dict["BLOCKBEGIN"], p[1])     #check if p[1] value i.e leaf value is required anywhere
	leaf2 = leaf_gen(Dict["BLOCKEND"], p[3])
	p[0] = Node(Dict["block"], [leaf1, p[2], leaf2])


def p_block_statements_opt(p):
	'''block_statements_opt : block_statements
							| empty '''
	p[0] = Node(Dict["block_statements_opt"], [p[1]])

def p_block_statements(p):
	'''block_statements : block_statement
						| block_statements block_statement'''
	if (len(p) == 3):
		p[0] = Node(Dict["block_statements"], [p[1], p[2]])
	else:
		p[0] = Node(Dict["block_statements"], [p[1]])

def p_block_statement(p):
	'''block_statement : local_variable_declaration_statement
						 | statement
						 | class_declaration
						 | SingletonObject
						 | method_declaration'''
	p[0] = Node(Dict["block_statement"], [p[1]])

#end of block definitions


#Expression definitions


def p_expression(p):
	'''expression : assignment_expression'''
	p[0] = Node(Dict["expression"], [p[1]])


def p_expression_optional(p):
	'''expression_optional : expression
						   | empty'''
	p[0] = Node(Dict["expression_optional"], [p[1]])

def p_assignment_expression(p):
		'''assignment_expression : assignment
								 | conditional_or_expression
								 | if_else_expression '''
		p[0] = Node(Dict["assignment_expression"], [p[1]])

def p_if_else_expression(p):
	'''if_else_expression : KEYWORD_IF LPAREN expression RPAREN expression KEYWORD_ELSE expression'''
	leaf1 = leaf_gen(Dict["IF"],p[1])
	leaf2 = leaf_gen(Dict["PARALEFT"],p[2])
	leaf3 = leaf_gen(Dict["PARARIGHT"],p[4])
	leaf4 = leaf_gen(Dict["ELSE"],p[6])
	p[0] = Node(Dict["if_else_expression"],[leaf1,leaf2,p[3],leaf3,p[5],leaf4,p[7]])


# ASSIGNMENT
def p_assignment(p):
		'''assignment : valid_variable assignment_operator assignment_expression'''
		p[0] = Node(Dict["assignment"], [p[1], p[2], p[3]])

def p_valid_variable(p):
		'''valid_variable : name
						  | array_access'''
		p[0] = Node(Dict["valid_variable"], [p[1]])

def p_array_access(p):
		'''array_access : name dimension'''
		p[0] = Node(Dict["array_access"], [p[1], p[2]])

def p_dimension(p):
	'''dimension : dimension LBRAC expression RBRAC
				 | LBRAC expression RBRAC '''
	if len(p)==5 :
		leaf1 = leaf_gen(Dict["LBRAC"],p[2])
		leaf2 = leaf_gen(Dict["RBRAC"],p[4])
		p[0] = Node(Dict["dimension"],[p[1],leaf1,p[3],leaf2])
	else:
		leaf1 = leaf_gen(Dict["LBRAC"],p[1])
		leaf2 = leaf_gen(Dict["RBRAC"],p[3])
		p[0] = Node(Dict["dimension"],[leaf1,p[2],leaf2]) 

def p_assignment_operator(p):
		'''assignment_operator :    ASOP 
							   | TIMES_ASSIGN
                               | DIVIDE_ASSIGN
                               | REMAINDER_ASSIGN
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | LSHIFT_ASSIGN
                               | RSHIFT_ASSIGN
                               | AND_ASSIGN
                               | OR_ASSIGN
                               | XOR_ASSIGN'''

		child1 = leaf_gen(Dict["ASSIGN_OP"], p[1])
		p[0] = Node(Dict["assignment_operator"], [leaf1])  



# OR(||) has least precedence, and OR is left assosiative 
# a||b||c => first evaluate a||b then (a||b)||c
def p_conditional_or_expression(p):
		'''conditional_or_expression : conditional_and_expression
									 | conditional_or_expression OR conditional_and_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["conditional_or_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["OR"], p[2])
			p[0] = Node(Dict["conditional_or_expression"], [p[1], leaf1, p[3]])

# AND(&&) has next least precedence, and AND is left assosiative 
# a&&b&&c => first evalutae a&&b then (a&&b)&&c

def p_conditional_and_expression(p):
		'''conditional_and_expression : inclusive_or_expression
									  | conditional_and_expression AND inclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["conditional_and_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["AND"], p[2])
			p[0] = Node(Dict["conditional_and_expression"], [p[1], leaf1, p[3]])

def p_inclusive_or_expression(p):
		'''inclusive_or_expression : exclusive_or_expression
								   | inclusive_or_expression OR_BITWISE exclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["inclusive_or_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["OR_BITWISE"], p[2])
			p[0] = Node(Dict["inclusive_or_expression"], [p[1], leaf1, p[3]])

def p_exclusive_or_expression(p):
		'''exclusive_or_expression : and_expression
								   | exclusive_or_expression XOR and_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["exclusive_or_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["XOR"], p[2])
			p[0] = Node(Dict["exclusive_or_expression"], [p[1], leaf1, p[3]])


def p_and_expression(p):
		'''and_expression : equality_expression
						  | and_expression AND_BITWISE equality_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["and_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["AND_BITWISE"], p[2])
			p[0] = Node(Dict["and_expression"], [p[1], leaf1, p[3]])

def p_equality_expression(p):
		'''equality_expression : relational_expression
								| equality_expression EQUAL relational_expression
								| equality_expression NEQUAL relational_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["relational_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["EqualityOp"], p[2])
			p[0] = Node(Dict["relational_expression"], [p[1], leaf1, p[3]])
	 

def p_relational_expression(p):
		'''relational_expression : shift_expression
								 | relational_expression GREATER shift_expression
								 | relational_expression LESS shift_expression
								 | relational_expression GEQ shift_expression
								 | relational_expression LEQ shift_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["relational_expression"], [p[1]])
		else:
			child1 = leaf_gen(Dict["RelationalOp"], p[2])
			p[0] = Node(Dict["relational_expression"], [p[1], leaf1, p[3]])
	 

def p_shift_expression(p):
				'''shift_expression : additive_expression
									| shift_expression LSHIFT additive_expression
									| shift_expression RSHIFT additive_expression'''
				if len(p) == 2:
					p[0] = Node(Dict["shift_expression"], [p[1]])
				else:
					child1 = leaf_gen(Dict["ShiftOp"], p[2])
					p[0] = Node(Dict["shift_expression"], [p[1], leaf1, p[3]])


#to do dict

def p_additive_expression(p):
		'''additive_expression : multiplicative_expression
								 | additive_expression PLUS multiplicative_expression
								 | additive_expression MINUS multiplicative_expression'''
		if len(p) == 2:
			p[0] = Node("additive_expression", [p[1]])
		else:
			child1 = create_leaf("AddOp", p[2])
			p[0] = Node("additive_expression", [p[1], child1, p[3]])

def p_multiplicative_expression(p):
		'''multiplicative_expression : unary_expression
									 | multiplicative_expression TIMES unary_expression
									 | multiplicative_expression DIVIDE unary_expression
									 | multiplicative_expression REMAINDER unary_expression'''
		if len(p) == 2:
			p[0] = Node("multiplicative_expression", [p[1]])
		else:
			child1 = create_leaf("MultOp", p[2])
			p[0] = Node("multiplicative_expression", [p[1], child1, p[3]])

def p_unary_expression(p):
		'''unary_expression : PLUS unary_expression
							| MINUS unary_expression
							| unary_expression_not_plus_minus'''
		if len(p) == 3:
			child1 = create_leaf("UnaryOp",p[1])
			p[0] = Node("unary_expression", [child1, p[2]])
		else:
			p[0] = Node("unary_expression", [p[1]])







def p_SimpleLiteral(p):
	'''SimpleLiteral : ['-']INTEGER_LITS
					 | [] '''







def empty(p):
	'''empty : '''
	p[0] = Node(Dic["empty"])
