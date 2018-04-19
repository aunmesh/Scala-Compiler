#symbolTable is a dictionary of lists. Name and type
dict_symboltable={}

def getscope(id):
		global dict_symboltable
		return dict_symboltable[id]

def addtemp(scope, temp):
	scope.templist.append(temp)

def check_validity(var,scope,vartype):
	if var in scope.table:
		return (scope.table[var])['place']
	else :
		if scope.pid == 0:
			print vartype ,var,' not declared.'
			raise Exception("Correct the Semantics :P")

		return check_validity(var, getscope(scope.pid), vartype)
def get_dict(var,scope):
	if var in scope.table:
		return (scope.table[var])
	else :
		if scope.pid == 0:
			print var,' not declared.'
			raise Exception("Correct the Semantics :P")

		return get_dict(var, getscope(scope.pid))

class Env:
	tablecount = 1
	def __init__(self, prev_env = None, name = None,templist = [], objecttype = None):
		self.table = {}
		self.id = Env.tablecount
		dict_symboltable[Env.tablecount] = self
		Env.tablecount += 1
		if prev_env == None:
			self.pid = 0
		else:
			self.pid = prev_env.id
		self.name = name
		self.objecttype = objecttype
		self.templist = list(templist)

	def addentry(self, dic):
		if dic['name'] in self.table:
			print 'Error: Entry already present - ( ' + name + ' )'
			assert(False)
		else:
			self.table[dic['name']]= dic

	def ispresent(self, name):
		if name in self.table:
			return True
		else:
			return False

	def getid(self):
		return self.id

TAC = []
TAC.append([])
SCOPE = Env(objecttype = "global", name = 'global')
PSCOPE = SCOPE
CSCOPE = SCOPE
nextquad = 1
nexttemp = 0
nextlabel = 0

class Node(object):
	gid = 1
	def __init__(self,name,children,value=None,argumentList=None,place=None,quad=None):
		self.name = name
		self.children = children
		self.id=Node.gid
		self.value=value
		self.argumentList=argumentList
		self.trueList = []
		self.falseList = []
		self.nextList = []
		self.quad = quad
		self.place=place
		self.type = None
		Node.gid+=1

def create_leaf(name1,name2):
		leaf1 = Node(name2,[])
		leaf2 = Node(name1,[leaf1])
		return leaf2

def backpatch(patchList, quadno):
	for i in patchList:
		TAC[i][1] = quadno

def newtemp():
	global nexttemp
	nexttemp += 1
	return 't' + str(nexttemp)

def newlabel():
	global nextlabel
	nextlabel += 1
	return 'fun' + str(nextlabel)

def emit(emitList):
	global nextquad
	TAC.append(emitList)
	nextquad += 1

def p_program_structure(p):
	'''ProgramStructure : ProgramStructure  class_and_objects
										| class_and_objects '''
	if len(p) == 3:
		p[0] = Node("ProgramStructure", [p[1], p[2]])
	else:
		p[0] = Node("ProgramStructure", [p[1]])

def p_class_and_objects(p):
	'''class_and_objects : SingletonObject'''
	p[0] = Node("class_and_objects", [p[1]])

def p_SingletonObject(p):
	'SingletonObject : ObjectDeclare block'
	p[0] = Node("SingletonObject", [p[1], p[2]])
	global SCOPE
	global CSCOPE
	tempdict = {}
	tempdict['name'] = p[1].place
	tempdict['type'] = 'object'
	SCOPE.addentry(tempdict)

def p_object_declare(p):
	'''ObjectDeclare : KEYWORD_OBJECT IDENTIFIER '''
	child1 = create_leaf("KEYWORD_OBJECT", p[1])
	child2 = create_leaf("IDENTIFIER", p[2])
	p[0] = Node("ObjectDeclare", [child1, child2], place = p[2])

# BLOCK DEFINITION
def p_block(p):
	'''block : start_scope block_statements_opt end_scope '''
	p[0] = Node("block", [p[1], p[2], p[3]])
	p[0].nextList = p[2].nextList

def p_start_scope(p):
	'''start_scope : BLOCKBEGIN'''
	child1 = create_leaf("BLOCKBEGIN", p[1])
	p[0] = Node("start_scope", [child1])

	global SCOPE
	global CSCOPE

	CSCOPE = Env(SCOPE)
	SCOPE = CSCOPE

def p_end_scope(p):
	'''end_scope : BLOCKEND'''
	child1 = create_leaf("BLOCKBEGIN", p[1])
	p[0] = Node("start_scope", [child1])

	global SCOPE

	SCOPE = getscope(SCOPE.pid)

def p_block_statements_opt(p):
	'''block_statements_opt : block_statements
							| empty '''
	p[0] = Node("block_statements_opt", [p[1]])
	p[0].nextList = p[1].nextList

def p_block_statements(p):
	'''block_statements : block_statement
						| block_statements marker block_statement'''
	if len(p) == 2:
		p[0] = Node("block_statement", [p[1]])
		p[0].nextList = p[1].nextList
	else:
		p[0] = Node("block_statements", [p[1], p[2], p[3]])
		backpatch(p[1].nextList, p[2].quad)
		p[0].nextList = p[3].nextList

def p_block_statement(p):
	'''block_statement : local_variable_declaration_statement
						 | statement
						 | SingletonObject
						 | method_declaration'''
	p[0] = Node("block_statement", [p[1]])
	p[0].nextList = p[1].nextList

# EXPRESSION
def p_expression(p):
	'''expression : assignment_expression'''
	p[0] = Node("expression", [p[1]], place = p[1].place)
	p[0].type = p[1].type
	p[0].value = p[1].value
	p[0].trueList = p[1].trueList
	p[0].falseList = p[1].falseList

def p_expression_optional(p):
	'''expression_optional : expression
						   | empty'''
	p[0] = Node("expression_optional", [p[1]], place = p[1].place)
	p[0].trueList = p[1].trueList
	p[0].falseList = p[1].falseList
	p[0].type = p[1].type
def p_assignment_expression(p):
		'''assignment_expression : assignment
								 | conditional_or_expression'''
		p[0] = Node("assignment_expression", [p[1]], place = p[1].place)
		p[0].value = p[1].value
		p[0].trueList = p[1].trueList
		p[0].falseList = p[1].falseList
		p[0].type = p[1].type
# def p_if_else_expression(p):
# 	'''if_else_expression : KEYWORD_IF LPAREN expression RPAREN expression KEYWORD_ELSE expression'''
# 	child1 = create_leaf("IF",p[1])
# 	child2 = create_leaf("LPAREN",p[2])
# 	child3 = create_leaf("RPAREN",p[4])
# 	child4 = create_leaf("ELSE",p[6])
# 	p[0] = Node("if_else_expression",[child1,child2,p[3],child3,p[5],child4,p[7]])

# ASSIGNMENT
def p_assignment(p):
		'''assignment : valid_variable assignment_operator assignment_expression'''
		p[0] = Node("assignment", [p[1], p[2], p[3]])
		if(p[1].type != p[3].type):
			# print p[1].type, p[3].type,p.lexer.lineno
			raise Exception("Type mismatch in assignment in line",p.lexer.lineno)

		if p[2].place == '=':
			emit(['=',p[1].place,p[3].place])
		else:
			emit([p[2].place[:-1],p[1].place,p[1].place,p[3].place])

		if '[' in p[1].name:
			emit(['=',p[1].name,p[1].place])

def p_valid_variable(p):
		'''valid_variable : name'''
		p[0] = Node("valid_variable", [p[1]],place = p[1].place)
		global SCOPE
		tempvar = check_validity(p[1].place, SCOPE, 'variable')
		p[0].type = p[1].type
		p[0].place = tempvar

def p_valid_variable1(p):
		'''valid_variable : array_access'''
		p[0] = Node("valid_variable", [p[1]],place = p[1].place)
		p[0].type = p[1].type
		p[0].name = p[1].name

def p_valid_variables(p):
	'''valid_variables : valid_variables COMMA valid_variable
						| valid_variable'''
	if len(p) == 2:
		p[0] = Node("valid_variables",[p[1]])
		p[0].place = [p[1].place]
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("valid_variables",[p[1],child1,p[3]])
		p[0].place = p[1].place + [p[3].place]

def p_array_access(p):
		'''array_access : name dimension'''
		p[0] = Node("array_access", [p[1], p[2]])
		global SCOPE
		d = get_dict(p[1].place, SCOPE)
		if d['type'] != "array":
			raise Exception(p[1].place, "is not an array in line",p.lexer.lineno)
		tempvar = check_validity(p[1].place, SCOPE, 'variable')
		newvar = newtemp()
		addtemp(SCOPE,newvar)
		p[0].place = newvar
		p[0].name = tempvar + ' ' + p[2].place
		p[0].type = 'Int'
		emit(['=',p[0].place,p[0].name])

def p_dimension(p):
	'''dimension : LBRAC expression RBRAC '''
	child1 = create_leaf("LBRAC",p[1])
	child2 = create_leaf("RBRAC",p[3])
	if p[2].type != 'Int':
		raise Exception("The access element must be an integer in line ",p.lexer.lineno)
	p[0] = Node("dimension",[child1,p[2],child2])
	p[0].place = '[ ' + p[2].place + ' ]'

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

		child1 = create_leaf("ASSIGN_OP", p[1])
		p[0] = Node("assignment_operator", [child1],place = p[1])


# OR(||) has least precedence, and OR is left assosiative
# a||b||c => first evaluate a||b then (a||b)||c
def p_marker(p):
	'''marker : empty '''
	global nextquad
	p[0] = Node("marker", [p[1]],quad = nextquad)

def p_narker(p):
	'''narker : empty '''
	global nextquad
	p[0] = Node("narker", [p[1]])
	p[0].nextList.append(nextquad)
	emit(['goto',None])

def p_conditional_or_expression(p):
		'''conditional_or_expression : conditional_and_expression
									 | conditional_or_expression OR marker conditional_and_expression'''
		if len(p) == 2:
			p[0] = Node("conditional_or_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("OR", p[2])
			p[0] = Node("conditional_or_expression", [p[1], child1, p[3],p[4]])
			if p[1].type != p[4].type:
				raise Exception("Type mismatch in OR expression in line ",p.lexer.lineno)
			else:
				p[0].type = p[1].type
			backpatch(p[1].falseList, p[3].quad)
			p[0].trueList = p[1].trueList + p[4].trueList
			p[0].falseList = p[4].falseList


# AND(&&) has next least precedence, and AND is left assosiative
# a&&b&&c => first evalutae a&&b then (a&&b)&&c

def p_conditional_and_expression(p):
		'''conditional_and_expression : inclusive_or_expression
									  | conditional_and_expression AND marker inclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node("conditional_and_expression", [p[1]], place = p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("AND", p[2])
			p[0] = Node("conditional_and_expression", [p[1], child1, p[3], p[4]])
			if p[1].type != p[4].type:
				# print p[1].type, p[3].type
				raise Exception("Type mismatch in AND expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
			backpatch(p[1].trueList, p[3].quad)
			p[0].falseList = p[1].falseList + p[4].falseList
			p[0].trueList = p[4].trueList

def p_inclusive_or_expression(p):
		'''inclusive_or_expression : exclusive_or_expression
								   | inclusive_or_expression OR_BITWISE exclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node("inclusive_or_expression", [p[1]], place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:

			child1 = create_leaf("OR_BITWISE", p[2])
			tempvar = newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([ p[2],tempvar, p[1].place, p[3].place])
			p[0] = Node("inclusive_or_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in Bitwise OR expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
def p_exclusive_or_expression(p):
		'''exclusive_or_expression : and_expression
								   | exclusive_or_expression XOR and_expression'''
		if len(p) == 2:
			p[0] = Node("exclusive_or_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("XOR", p[2])
			tempvar = newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[2],tempvar,p[1].place,p[3].place])
			p[0] = Node("exclusive_or_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in XOR expression in line", p.lexer.lineno)
			else:
				p[0].type = p[1].type
def p_and_expression(p):
		'''and_expression : equality_expression
						  | and_expression AND_BITWISE equality_expression'''
		if len(p) == 2:
			p[0] = Node("and_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("AND_BITWISE", p[2])
			tempvar=newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[2],tempvar,p[1].place,p[3].place])
			p[0] = Node("and_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in Bitwise AND expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
def p_equality_expression(p):
		'''equality_expression : relational_expression
								| equality_expression EQUAL relational_expression
								| equality_expression NEQUAL relational_expression'''
		if len(p) == 2:
			p[0] = Node("relational_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("EqualityOp", p[2])
			global nextquad
			p[0] = Node("relational_expression", [p[1], child1, p[3]])
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in equality expression in line ", p.lexer.lineno)
			else:
				p[0].type = p[1].type
			p[0].trueList.append(nextquad)
			emit(["ifgoto",None,p[2],p[1].place,p[3].place])
			p[0].falseList.append(nextquad)
			emit(["goto",None])

def p_relational_expression(p):
		'''relational_expression : shift_expression
								 | relational_expression GREATER shift_expression
								 | relational_expression LESS shift_expression
								 | relational_expression GEQ shift_expression
								 | relational_expression LEQ shift_expression'''
		if len(p) == 2:
			p[0] = Node("relational_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("RelationalOp", p[2])
			global nextquad
			p[0] = Node("relational_expression", [p[1], child1, p[3]])
			# print "relational",p[1].type, p[3].type
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in relational expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
			p[0].trueList.append(nextquad)
			emit(["ifgoto",None,p[2],p[1].place,p[3].place])
			p[0].falseList.append(nextquad)
			emit(["goto",None])


def p_shift_expression(p):
		'''shift_expression : additive_expression
							| shift_expression LSHIFT additive_expression
							| shift_expression RSHIFT additive_expression'''
		if len(p) == 2:
			p[0] = Node("shift_expression", [p[1]],place=p[1].place)
			p[0].trueList = p[1].trueList
			p[0].falseList = p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("ShiftOp", p[2])
			tempvar = newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[2],tempvar,p[1].place,p[3].place])
			p[0] = Node("shift_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in shift expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type

def p_additive_expression(p):
		'''additive_expression : multiplicative_expression
								 | additive_expression PLUS multiplicative_expression
								 | additive_expression MINUS multiplicative_expression'''
		if len(p) == 2:
			p[0] = Node("additive_expression", [p[1]],place=p[1].place)
			p[0].trueList=p[1].trueList
			p[0].falseList=p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("AddOp", p[2])
			tempvar=newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[2],tempvar,p[1].place,p[3].place])
			p[0] = Node("additive_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in Additive expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
def p_multiplicative_expression(p):
		'''multiplicative_expression : unary_expression
									 | multiplicative_expression TIMES unary_expression
									 | multiplicative_expression DIVIDE unary_expression
									 | multiplicative_expression REMAINDER unary_expression'''
		if len(p) == 2:
			p[0] = Node("multiplicative_expression", [p[1]],place=p[1].place)
			p[0].trueList=p[1].trueList
			p[0].falseList=p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("MultOp", p[2])
			tempvar=newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[2],tempvar,p[1].place,p[3].place])
			p[0] = Node("multiplicative_expression", [p[1], child1, p[3]],place=tempvar)
			if p[1].type != p[3].type:
				raise Exception("Type mismatch in Multiplicative expression in line",p.lexer.lineno)
			else:
				p[0].type = p[1].type
def p_unary_expression(p):
		'''unary_expression : PLUS unary_expression
							| MINUS unary_expression
							| unary_expression_not_plus_minus'''
		if len(p) == 3:
			child1 = create_leaf("UnaryOp",p[1])
			tempvar = newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit([p[1],tempvar,"0",p[2]])
			p[0].type = p[2].type
			p[0] = Node("unary_expression", [child1, p[2]],place=tempvar)
		else:
			p[0] = Node("unary_expression", [p[1]],place=p[1].place)
			p[0].trueList=p[1].trueList
			p[0].falseList=p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type


def p_unary_expression_not_plus_minus(p):
		'''unary_expression_not_plus_minus : base_variable_set
											 | TILDA unary_expression'''
		if len(p) == 2:
			p[0] = Node("unary_expression_not_plus_minus", [p[1]],place=p[1].place)
			p[0].trueList=p[1].trueList
			p[0].falseList=p[1].falseList
			p[0].value = p[1].value
			p[0].type = p[1].type
		else:
			child1 = create_leaf("Unary_1Op", p[1])
			tempvar=newtemp()
			global SCOPE
			addtemp(SCOPE, tempvar)
			emit(["=",p[1],tempvar,p[2]])
			p[0] = Node("unary_expression_not_plus_minus", [child1, p[2]],place=tempvar)
			p[0].trueList=p[2].trueList
			p[0].falseList=p[2].falseList
			p[0].type = p[2].type

def p_unary_expression_not_plus_minus1(p):
	'''unary_expression_not_plus_minus : NOT unary_expression'''
	child1 = create_leaf("Unary_1Op", p[1])
	p[0] = Node("unary_expression_not_plus_minus", [child1, p[2]])
	p[0].trueList=p[2].falseList
	p[0].falseList=p[2].trueList
	if p[2].type != "Boolean":
		raise Exception("NOT can only be used with boolean type. Invalid use with ", p[2].type,"in line ",p.lexer.lineno)
	else:
		p[0].type = p[2].type

def p_base_variable_set(p):
	'''base_variable_set : variable_literal
						 | LPAREN expression RPAREN'''
	if len(p) == 2:
		p[0] = Node("base_variable_set", [p[1]],place=p[1].place)
		p[0].trueList=p[1].trueList
		p[0].falseList=p[1].falseList
		p[0].value = p[1].value
		p[0].type = p[1].type
	else:
		child1 = create_leaf("LPAREN", p[1])
		child2 = create_leaf("RPAREN", p[3])
		p[0] = Node("base_variable_set", [child1, p[2], child2],place=p[2].place)
		p[0].trueList=p[2].trueList
		p[0].falseList=p[2].falseList
		p[0].type = p[2].type
def p_variableliteral(p):
		'''variable_literal : valid_variable
							| primary'''
		p[0] = Node("variable_literal", [p[1]],place=p[1].place)
		p[0].trueList=p[1].trueList
		p[0].falseList=p[1].falseList
		p[0].value = p[1].value
		p[0].type = p[1].type

# def p_cast_expression(p):
# 		'''cast_expression : LPAREN primitive_type RPAREN unary_expression'''
# 		child1 = create_leaf("LPAREN", p[1])
# 		child2 = create_leaf("RPAREN", p[3])
# 		p[0] = Node("cast_expression", [child1, p[2], child2, p[4]],place=p[4].place)
# 		p[0].trueList=p[2].trueList
# 		p[0].falseList=p[2].falseList
# 		p[0].
def p_primary(p):
		'''primary : literal
					| method_invocation'''
		p[0] = Node("primary", [p[1]],place=p[1].place)
		p[0].trueList=p[1].trueList
		p[0].falseList=p[1].falseList
		p[0].value = p[1].value
		p[0].type = p[1].type

def p_literal(p):
		'''literal : int_float
					| c_literal '''
		p[0] = Node("literal", [p[1]],place=p[1].place)
		p[0].trueList=p[1].trueList
		p[0].falseList=p[1].falseList
		p[0].value = p[1].value
		p[0].type = p[1].type


# def p_c_literal(p):
# 		'''c_literal : CHAR
# 					| STRING
# 					| KEYWORD_NULL'''
# 		child1 = create_leaf("LiteralConst",[p[1]])
# 		tempvar = newtemp()
# 		emit(["=",tempvar,p[1]])
# 		p[0] = Node("c_literal", [child1],place=tempvar)

def p_c_literal_binary_true(p):
		'''c_literal : BOOL_CONSTT'''
		child1 = create_leaf("BinaryConstTrue",[p[1]])
		p[0] = Node("c_literal", [child1])
		global nextquad
		p[0].trueList.append(nextquad)
		emit(["goto",None])
		p[0].type = "Boolean"

def p_c_literal_binary_false(p):
		'''c_literal : BOOL_CONSTF'''
		child1 = create_leaf("BinaryConstFalse",[p[1]])
		p[0] = Node("c_literal", [child1])
		global nextquad
		p[0].falseList.append(nextquad)
		emit(["goto",None])
		p[0].type = "Boolean"

def p_int_float(p):
		'''int_float : INT_NUMBER '''
		child1 = create_leaf("IntConst", p[1])
		p[0] = Node("int_float", [child1],place=p[1])
		p[0].value = p[1]
		p[0].type = "Int"

# FUNCTION CALL
def p_method_invocation(p): #type checking remaining
		'''method_invocation : name LPAREN argument_list_opt RPAREN '''
		child1 = create_leaf("LPAREN", p[2])
		child2 = create_leaf("RPAREN", p[4])
		p[0] = Node("method_invocation", [p[1], child1, p[3], child2])
		global SCOPE
		tempvar = check_validity(p[1].place,SCOPE, 'function')
		d= get_dict(p[1].place, SCOPE)
		tid = d['tid']
		paramtype=d['paramtype']
		# print "Method invocation",paramtype, p[3].type
		for i in range(0,len(p[3].type)):
			if p[3].type[i] != paramtype[i]:
				# print "Function parameter type",p[3].type[i], paramtype[i]
				raise Exception("Type of parameters mismatch in line",p.lexer.lineno)

		if d['type'] !='function':
			raise Exception(tempvar, " is not a function in line",p.lexer.lineno)
		p[0].type = d['returntype']
		if p[3].place is not None:
			if d['lenarg'] != len(p[3].place):
				raise Exception(" Insufficient arguments for",p[1].place,"in line ",p.lexer.lineno)
		else:
			if d['lenarg'] != 0:
				raise Exception(" Function ",p[1].place,"cannot take arguments in line",p.lexer.lineno)
		if p[3].place is not None:
			for i in p[3].place:
				emit(['param', i ])


		emit(['call', tempvar])
		p[0].place = newtemp()
		addtemp(SCOPE,p[0].place)
		emit(['=', p[0].place, 'return'])

def p_argument_list_opt(p):
		'''argument_list_opt : argument_list'''
		p[0] = Node("argument_list_opt", [p[1]])
		p[0].place = p[1].place
		p[0].type = p[1].type
def p_argument_list_opt2(p):
		'''argument_list_opt : empty'''
		p[0] = Node("argument_list_opt", [p[1]])
		p[0].type = ["Unit"]
def p_argument_list(p):
		'''argument_list : expression
						| argument_list COMMA expression'''
		if len(p) == 2:
			p[0] = Node("argument_list", [p[1]])
			p[0].place = [p[1].place]
			p[0].type = [p[1].type]
		else:
			child1 = create_leaf("COMMA", p[2])
			p[0] = Node("argument_list", [p[1], child1, p[3]])
			p[0].place = p[1].place + [p[3].place]
			p[0].type = p[1].type + [p[3].type]
# LOCAL VARIABLE DECLARATION

def p_declaration_keyword(p):
	'''declaration_keyword : KEYWORD_VAR
						   | KEYWORD_VAL '''
	child1 = create_leaf("KEYWORD_VAR/VAL", p[1])
	p[0] = Node("declaration_keyword", [child1], place = p[1])


def p_local_variable_declaration_statement(p):
			'''local_variable_declaration_statement : local_variable_declaration TERMINATOR '''
			child1 = create_leaf("STATE_END", p[2])
			p[0] = Node("local_variable_declaration_statement", [p[1], child1])
			p[0].type = p[1].type

def p_local_variable_declaration(p):
			'''local_variable_declaration : declaration_keyword variable_declaration_body'''
			p[0] = Node("local_variable_declaration", [ p[1], p[2]])
			p[0].type = p[2].type
def p_variable_declaration_initializer(p):
	'''variable_declaration_initializer : expression
										| array_initializer'''
	p[0] = Node("variable_declaration_initializer", [p[1]], place=p[1].place)
	p[0].type = p[1].type
	p[0].place = p[1].place

def p_variable_argument_list(p):
	''' variable_argument_list : variable_declaration_initializer
										| variable_argument_list COMMA variable_declaration_initializer'''
	if len(p) == 2:
		p[0] = Node("variable_argument_list", [p[1]])
		p[0].type = p[1].type
	else:
		child1 = create_leaf("COMMA", p[2])
		p[0] = Node("variable_argument_list", [p[1], child1, p[3]])
		p[0].type = p[3].type
def p_variable_declaration_body_1(p): # eg. var x:Int = 2; or var x = 2 or var x,y,z:Int = 2 or var x,y,z = 2;
	'''variable_declaration_body : identifiers COLON type ASOP  variable_declaration_initializer '''
	child1 = create_leaf("ASOP", p[4])
	child2 = create_leaf("COLON", p[2])
	p[0] = Node("variable_declaration_body", [p[1], child2, p[3], child1, p[5]])
	global SCOPE
	p[0].type = p[5].type
	for i in range(0,len(p[1].place)):
		tempdict = {}
		tempdict['name'] = p[1].place[i]
		tempdict['type'] = p[5].type
		tempdict['place'] = newtemp()
		tempdict['scopetype'] = 'local'

		if tempdict['type'] == 'newarray':
			tempdict['type'] = 'array'
			tempdict['size'] = int(p[5].place)
			emit(["Array", tempdict['place'], 4*int(tempdict['size'])])
		else:
			if tempdict['type'] == 'array':
				tempdict['size'] = len(p[5].place)
				emit(['Array', tempdict['place'], 4*int(tempdict['size'])])
				for j in range(0,tempdict['size']):
					emit(['=', tempdict['place'], '[', str(j), ']', p[5].place[j]])
			else:
				emit(['=' , tempdict['place'], p[5].place])
		SCOPE.addentry(tempdict)

def p_identifiers(p):
	''' identifiers : identifiers COMMA IDENTIFIER
					| IDENTIFIER'''
	if len(p)==2:
		child1 = create_leaf("IDENTIFIER",p[1])
		p[0] = Node("identifiers",[child1])
		p[0].place = [p[1]]
	else:
		child1 = create_leaf("COMMA",p[2])
		child2 = create_leaf("IDENTIFIER",p[3])
		p[0] = Node("identifiers",[p[1],child1,child2])
		p[0].place = p[1].place + [p[3]]
		p[0].type = p[1].type

# def p_variable_declaration_body_2(p): # eg. var (x:Int,y:Array[String],z) = (2,new Array[String](5),3);
# 	'''variable_declaration_body : LPAREN variable_list RPAREN ASOP LPAREN variable_argument_list RPAREN'''
# 	child1 = create_leaf("LPAREN", p[1])
# 	child2 = create_leaf("RPAREN", p[3])
# 	child3 = create_leaf("ASOP", p[4])
# 	child4 = create_leaf("LPAREN", p[5])
# 	child5 = create_leaf("RPAREN", p[7])
# 	p[0] = Node("variable_declaration_body", [child1, p[2], child2, child3, child4, p[6], child5])

def p_variable_list(p):					# eg. x:Int,y:Int,z:Int
	''' variable_list : variable_declarator_id
					  | variable_list COMMA variable_declarator_id'''
	if len(p)==2:
		p[0] = Node("variable_list",[p[1]])
		p[0].type = p[1].type
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("variable_list",[p[1],child1,p[3]])
		p[0].type = p[3].type

# def p_variable_dec(p):						# eg. x:Int or x
# 	''' variable_dec : IDENTIFIER type_opt'''
# 	child1 = create_leaf("IDENTIFIER",p[1])
# 	p[0] = Node("variable_dec",[child1,p[2]])

# def p_variable_declaration_body_3(p): # eg. var x,y,z = (a:Int) => a*a;  Notice, x,y,z are functions.
# 	''' variable_declaration_body : identifiers ASOP LPAREN fun_params RPAREN FUNTYPE expression'''

# 	child2 = create_leaf("ASOP", p[2])
# 	child3 = create_leaf("LPAREN", p[3])
# 	child4 = create_leaf("RPAREN", p[5])
# 	child5 = create_leaf("FUNTYPE", p[6])
# 	p[0] = Node("variable_declaration_body", [p[1], child2, child3, p[4], child4, child5,p[7]])


# def p_expr_opt(p):
# 	''' expr_opt : ASOP variable_declaration_initializer
# 				 | empty '''
# 	if len(p) > 2:
# 		child1 = create_leaf("ASOP",p[1])
# 		p[0] = Node("expr_opt",[child1,p[2]])
# 	else:
# 		p[0] = Node("expr_opt",[p[1]])


def p_variable_declarator_id(p):
	'''variable_declarator_id : IDENTIFIER COLON type'''
	child1 = create_leaf("IDENTIFIER", p[1])
	child2 = create_leaf("COLON", p[2])
	p[0] = Node("variable_declarator_id", [child1, child2, p[3]])
	p[0].type = p[3].type

def p_fun_variable_declarator_id(p):
	'''fun_variable_declarator_id : IDENTIFIER COLON type'''
	child1 = create_leaf("IDENTIFIER", p[1])
	child2 = create_leaf("COLON", p[2])
	p[0] = Node("fun_variable_declarator_id", [child1, child2, p[3]])
	p[0].place = p[1]
	p[0].type = p[3].type


#DATA_TYPES AND VARIABLE_TYPES
def p_type(p):
	'''type : primitive_type
			| reference_type '''
	p[0] = Node("type", [p[1]])
	p[0].type = p[1].type

def p_primitive_type(p):
	'''primitive_type : TYPE_INT'''
	child1 = create_leaf("TYPE", p[1])
	p[0] = Node("primitive_type", [child1])
	p[0].type = p[1]

def p_reference_type(p):
	'''reference_type : array_data_type'''
	p[0] = Node("reference_type", [p[1]])
	p[0].type = p[1].type


def p_array_data_type(p):
	'''array_data_type : KEYWORD_ARRAY LBRAC TYPE_INT RBRAC'''
	child1 = create_leaf("ARRAY", p[1])
	child2 = create_leaf("LBRAC", p[2])
	child3 = create_leaf("TYPE",p[3])
	child4 = create_leaf("RBRAC", p[4])
	p[0] = Node("array_data_type", [child1, child2, child3, child4])
	p[0].type = 'array'


#VARIABLE_NAMES
def p_name(p):
		'''name : simple_name
				| qualified_name'''
		p[0] = Node("name", [p[1]])
		p[0].value = p[1].value
		p[0].place = p[1].place
		p[0].type = p[1].type

def p_simple_name(p):
		'''simple_name : IDENTIFIER'''
		child1 = create_leaf("IDENTIFIER", p[1])
		p[0] = Node("simple_name", [child1])
		global SCOPE
		p[0].value = p[1]
		p[0].place = p[1]
		d = get_dict(p[1], SCOPE)
		# print d
		p[0].type = d['type']
def p_qualified_name(p):
		'''qualified_name : name INST simple_name'''
		child1 = create_leaf("DOT", p[2])
		p[0] = Node("qualified_name", [p[1], child1, p[3]])
		global SCOPE
		p[0].value = p[1].value + '.' + p[3].value
		p[0].place = p[1].place + '.' + p[3].place
		d = get_dict(p[3], SCOPE)
		p[0].type = d['type']

#INITIALIZERS
def p_array_initializer(p):
	''' array_initializer : KEYWORD_NEW KEYWORD_ARRAY LBRAC type RBRAC LPAREN conditional_or_expression RPAREN
												| KEYWORD_ARRAY LBRAC type RBRAC LPAREN argument_list RPAREN'''
	if len(p) == 9:
		child1 = create_leaf("NEW", p[1])
		child2 = create_leaf("ARRAY", p[2])
		child3 = create_leaf("LBRAC", p[3])
		child4 = create_leaf("RBRAC", p[5])
		child5 = create_leaf("LPAREN", p[6])
		child7 = create_leaf("RPAREN", p[8])

		p[0] = Node("array_initializer", [child1, child2, child3, p[4], child4, child5, p[6], child7])
		p[0].type = 'newarray'
		p[0].place = p[7].value

	elif len(p)==8:
		child2 = create_leaf("ARRAY", p[1])
		child3 = create_leaf("LBRAC", p[2])
		child4 = create_leaf("RBRAC", p[4])
		child5 = create_leaf("LPAREN", p[5])
		child7 = create_leaf("RPAREN", p[7])

		p[0] = Node("array_initializer", [child2, child3, p[3], child4, p[5],child7])
		p[0].type = 'array'
		p[0].place = p[6].place
	else:
		child1 = create_leaf("ARRAY", p[1])
		child2 = create_leaf("LPAREN", p[2])
		child3 = create_leaf("RPAREN", p[4])
		p[0] = Node("array_initializer", [child1, child2, p[3], child3])

# def p_class_initializer(p):
# 	''' class_initializer : KEYWORD_NEW name LPAREN argument_list_opt RPAREN '''
# 	child1 = create_leaf("NEW", p[1])
# 	child2 = create_leaf("LPAREN", p[3])
# 	child3 = create_leaf("RPAREN", p[5])
# 	p[0] = Node("class_initializer", [child1, p[2], child2, p[4], child3])
# 	p[0].place = p[4].place
# 	p[0].type = 'class'
# 	p[0].value = p[2].value

# STATEMENTS
def p_statement(p):
		'''statement : normal_statement marker
					 | if_then_statement marker
					 | if_then_else_statement marker
					 | while_statement marker
					 | do_while_statement marker
					 | for_statement marker'''
		p[0] = Node("statement", [p[1],p[2]])
		backpatch(p[1].nextList, p[2].quad)

def p_normal_statement(p):
	'''normal_statement : block marker
						| expression_statement marker
						| empty_statement marker
						| return_statement marker
						| switch_statement marker 
						| print_int marker
						| print_string marker
						| scan_int marker'''

	p[0] = Node("normal_statement", [p[1],p[2]])
	backpatch(p[1].nextList, p[2].quad)

def p_expression_statement(p):
	'''expression_statement : statement_expression TERMINATOR'''
	child1 = create_leaf("STATE_END", p[2])
	p[0] = Node("expression_statement", [p[1], child1])


def p_statement_expression(p):
	'''statement_expression : assignment
							| method_invocation'''

	p[0] = Node("statement_expression", [p[1]])
	p[0].place = p[1].place


#IF THEN STATEMENT
def p_if_then_statement(p):
	'''if_then_statement : KEYWORD_IF LPAREN expression RPAREN marker block'''
	child1 = create_leaf("IF",p[1])
	child2 = create_leaf("LPAREN",p[2])
	child3 = create_leaf("RPAREN",p[4])
	p[0] = Node("if_then_statement",[child1,child2,p[3],child3,p[5],p[6]])
	backpatch(p[3].trueList, p[5].quad)
	p[0].nextList = p[3].falseList + p[6].nextList

def p_if_then_else_statement(p):
		'''if_then_else_statement : KEYWORD_IF LPAREN expression RPAREN marker if_then_else_intermediate narker KEYWORD_ELSE marker block'''
		child1 = create_leaf("IF", p[1])
		child2 = create_leaf("LPAREN", p[2])
		child3 = create_leaf("RPAREN", p[4])
		child4 = create_leaf("ELSE", p[8])
		p[0] = Node("if_then_else_statement", [child1, child2, p[3], child3, p[5], p[6],p[7], child4, p[9],p[10]])
		backpatch(p[3].trueList, p[5].quad)
		backpatch(p[3].falseList, p[9].quad)
		p[0].nextList = p[6].nextList + p[7].nextList + p[10].nextList


def p_if_then_else_statement_precedence(p):
		'''if_then_else_statement_precedence : KEYWORD_IF LPAREN expression RPAREN marker if_then_else_intermediate narker KEYWORD_ELSE marker if_then_else_intermediate'''
		child1 = create_leaf("IF", p[1])
		child2 = create_leaf("LPAREN", p[2])
		child3 = create_leaf("RPAREN", p[4])
		child4 = create_leaf("ELSE", p[8])
		p[0] = Node("if_then_else_statement_precedence", [child1, child2, p[3], child3, p[5], p[6],p[7],child4, p[9],p[10]])
		backpatch(p[3].trueList, p[5].quad)
		backpatch(p[3].falseList, p[9].quad)
		p[0].nextList = p[6].nextList + p[7].nextList + p[10].nextList


def p_if_then_else_intermediate(p):
		'''if_then_else_intermediate : normal_statement
									 | if_then_else_statement_precedence'''
		p[0] = Node("if_then_else_intermediate", [p[1]])
		p[0].nextList = p[1].nextList

# WHILE_LOOP
def p_while_statement(p):
	'''while_statement : KEYWORD_WHILE LPAREN marker expression RPAREN marker block'''
	child1 = create_leaf("WHILE", p[1])
	child2 = create_leaf("LPAREN", p[2])
	child3 = create_leaf("RPAREN", p[5])
	p[0] = Node("while_statement", [child1, child2, p[3], p[4],child3, p[6],p[7]])
	backpatch(p[4].trueList, p[6].quad)
	backpatch(p[6].nextList, p[3].quad)
	p[0].nextList = p[4].falseList
	emit(['goto', p[3].quad])

#DO_WHILE_LOOP
def p_do_while_statement(p):
	'''do_while_statement : KEYWORD_DO marker block KEYWORD_WHILE LPAREN marker expression RPAREN TERMINATOR '''
	child1 = create_leaf("DO", p[1])
	child2 = create_leaf("WHILE", p[4])
	child3 = create_leaf("LPAREN", p[5])
	child4 = create_leaf("RPAREN", p[8])
	child5 = create_leaf("STATE_END", p[9])
	p[0] = Node("do_while_statement", [child1, p[2], p[3], child2, child3, p[6], p[7], child4, child5])
	backpatch(p[3].nextList, p[6].quad)
	backpatch(p[7].trueList, p[2].quad)
	p[0].nextList = p[7].falseList

# FOR_LOOP
def p_for_statement(p):
	'''for_statement : KEYWORD_FOR LPAREN for_update marker RPAREN block'''
	child1 = create_leaf ("FOR",p[1])
	child2 = create_leaf ("LPAREN",p[2])
	child3 = create_leaf ("RPAREN",p[4])
	p[0] = Node("for_statement",[child1,child2,p[3],child3,p[5],p[6]])
	backpatch(p[3].trueList, p[4].quad)
	backpatch(p[6].nextList, p[3].quad)
	emit(['goto', p[3].quad])
	p[0].nextList = p[3].falseList

def p_for_update(p):
	''' for_update : for_loop marker for_part marker for_step_opts'''
	p[0]=Node("for_update",[p[1],p[2],p[3], p[4], p[5]])
	emit(['+', p[1].place , p[1].place, p[5].place])
	emit(['goto', p[2].quad])
	backpatch(p[3].nextList, nextquad)
	p[0].trueList.append(nextquad)
	emit(['ifgoto', 'None', p[3].place, p[1].place, p[3].name])
	p[0].falseList.append(nextquad)
	emit(['goto', 'None'])
	p[0].quad = p[4].quad

def p_for_loop(p):
	''' for_loop : IDENTIFIER CHOOSE expression'''

	child1 = create_leaf("IDENTIFIER",p[1])
	child2 = create_leaf("CHOOSE",p[2])
	p[0] = Node("for_loop_st",[child1,child2,p[3]])
	global nextquad
	global SCOPE
	tempvar = check_validity(p[1],SCOPE, 'variable')
	emit(['=', tempvar, p[3].place])
	p[0].place = tempvar

def p_for_part(p):
	'''for_part : for_untilTo expression '''
	p[0] = Node("for_part",[p[1],p[2]])
	p[0].place = p[1].place
	p[0].name = p[2].place
	global nextquad
	p[0].nextList.append(nextquad)
	emit(['goto', 'None'])

def p_for_untilTo1(p):
	'''for_untilTo : KEYWORD_UNTIL '''

	child1 = create_leaf("UNTIL_TO",p[1])
	p[0]=Node("for_untilTo",[child1])
	p[0].place = '<'

def p_for_untilTo2(p):
	'''for_untilTo : KEYWORD_TO '''

	child1 = create_leaf("UNTIL_TO",p[1])
	p[0]=Node("for_untilTo",[child1])
	p[0].place = '<='

def p_for_step_opts(p):
	''' for_step_opts : KEYWORD_BY expression
										| empty'''
	if len(p)==2:
		p[0]=Node("for_step_opts",[p[1]])
		p[0].place = '1'
	else :
		child1 = create_leaf("BY",p[1])
		p[0]=Node("for_step_opts",[child1,p[2]])
		p[0].place = p[2].place

def p_switch_statement(p):
		'''switch_statement : expression KEYWORD_MATCH switch_block marker'''
		child1 = create_leaf("MATCH", p[2])
		p[0] = Node("switch_statement", [p[1], child1, p[3]])

		for i in range(0,len(p[3].place)):
			emit(['ifgoto', p[3].quad[i], '==', p[1].place, p[3].place[i]])

		global nextquad

		backpatch(p[3].nextList, nextquad)


def p_switch_block(p):
		'''switch_block : BLOCKBEGIN BLOCKEND '''
		child1 = create_leaf("BLOCKBEGIN", p[1])
		child2 = create_leaf("BLOCKEND", p[2])
		p[0] = Node("switch_block", [child1, child2])


def p_switch_block2(p):
		'''switch_block : BLOCKBEGIN switch_block_statements BLOCKEND '''
		child1 = create_leaf("BLOCKBEGIN", p[1])
		child2 = create_leaf("BLOCKEND", p[3])
		p[0] = Node("switch_block", [child1, p[2], child2])
		p[0].place = p[2].place
		p[0].quad = p[2].quad
		p[0].nextList = p[2].nextList

def p_switch_block_statements(p):
		'''switch_block_statements : switch_block_statement marker
								   | switch_block_statements switch_block_statement marker'''
		if len(p) == 3:
		  p[0] = Node("switch_block_statements", [p[1], p[2]])
		  p[0].place = [p[1].place]
		  p[0].quad = [p[1].quad]
		  p[0].nextList = p[1].trueList
		  backpatch(p[1].nextList,p[2].quad)
		else:
		  p[0] = Node("switch_block_statements", [p[1], p[2], p[3]])
		  backpatch(p[2].nextList,p[3].quad)
		  p[0].place = p[1].place + [p[2].place]
		  p[0].quad = p[1].quad + [p[2].quad]
		  p[0].nextList = p[1].nextList + p[2].trueList


def p_switch_block_statement(p):
		'''switch_block_statement : switch_label narker marker block narker'''
		p[0] = Node("switch_block_statement", [p[1], p[2], p[3], p[4], p[5]])
		p[0].place = p[1].place
		p[0].quad = p[3].quad
		p[0].nextList = p[2].nextList
		p[0].trueList = p[4].nextList + p[5].nextList

def p_switch_label(p):
		'''switch_label : KEYWORD_CASE expression FUNTYPE '''
		child1 = create_leaf("CASE", p[1])
		child2 = create_leaf("FUNTYPE", p[3])
		p[0] = Node("switch_label", [child1, p[2], child2])
		p[0].place = p[2].place


#EMPTY STATEMENT
def p_empty_statement(p):
				'''empty_statement : TERMINATOR '''
				child1 = create_leaf("STATE_END", p[1])
				p[0] = Node("empty_statement", [child1])

#RETURN STATEMENT
def p_return_statement(p):
				'''return_statement : KEYWORD_RETURN expression_optional TERMINATOR '''
				child1 = create_leaf("RETURN", p[1])
				child2 = create_leaf("STATE_END", p[3])
				p[0] = Node("return_statement", [child1, p[2], child2])
				global SCOPE
				dic = {}
				dic['name'] = 'return'
				dic['place'] = p[2].place
				dic['type'] = p[2].type
				dic['scopetype'] = 'local'
				SCOPE.addentry(dic)
				if p[2].place != None:
					emit(['ret', p[2].place])


def p_scan_int(p):
	'''scan_int : KEYWORD_SCAN IDENTIFIER'''
	child1 = create_leaf("KEYWORD_SCAN",p[1])
	child2 = create_leaf("IDENTIFIER",p[2])
	p[0] = Node("scan_statement", [child1,child2])
	tempvar = check_validity(p[2],SCOPE, 'variable')
	emit(['scan',tempvar])

def p_print_int(p):
	'''print_int : KEYWORD_PRINT valid_variables'''
	child1 = create_leaf("KEYWORD_PRINT",p[1])
	p[0] = Node("print_statement", [child1,p[2]])
	for i in range(len(p[2].place)):
		# if '[' in (p[2].place)[i]:
		# 	tempvar = newtemp();
		# 	emit(['=',tempvar, (p[2].place)[i]])
		# else:
		tempvar = (p[2].place)[i]
		
		emit(['print',tempvar])

def p_println_int(p):
	'''print_int : KEYWORD_PRINTLN valid_variables'''
	child1 = create_leaf("KEYWORD_PRINTLN",p[1])
	p[0] = Node("print_statement", [child1,p[2]])
	for i in range(len(p[2].place)):
		# if '[' in (p[2].place)[i]:
		# 	tempvar = newtemp();
		# 	emit(['=',tempvar, (p[2].place)[i]])
		# else:
		tempvar = (p[2].place)[i]
		
		emit(['print',tempvar])
	emit(['print newline'])

def p_print_string(p):
	'''print_string : KEYWORD_PRINT STRING'''
	child1 = create_leaf("KEYWORD_PRINT",p[1])
	child2 = create_leaf("STRING",p[2])
	p[0] = Node("print_statement", [child1,child2])
	tempvar = newtemp()
	emit(['=s',tempvar,'"',p[2],'"'])
	emit(['print',tempvar])


def p_println_string(p):
	'''print_string : KEYWORD_PRINTLN STRING'''
	child1 = create_leaf("KEYWORD_PRINTLN",p[1])
	child2 = create_leaf("STRING",p[2])
	p[0] = Node("print_statement", [child1,child2])
	tempvar = newtemp()
	emit(['=s',tempvar,'"',p[2],'"'])
	emit(['print',tempvar])
	emit(['print newline'])


def p_method_declaration(p):
		'''method_declaration : method_header method_body'''
		p[0] = Node("method_declaration", [p[1], p[2]])


def p_method_header(p):
		'''method_header : method_header_name func_arg_start fun_params_opt RPAREN COLON method_return_type ASOP'''
		child2 = create_leaf("RPAREN", p[4])
		child3 = create_leaf("COLON", p[5])
		child4 = create_leaf("ASSIGN", p[7])
		global SCOPE

		if p[3].place != None:
			paramtype = list(p[3].type)
			for i in range(0,len(p[3].place)):
				tempdict = {}
				tempdict['name'] = p[3].place[i]
				tempdict['type'] = p[3].type[i]
				tempdict['scopetype'] = 'param'
				tempdict['paramno'] = i + 1
				tempdict['place'] = newtemp()
				SCOPE.addentry(tempdict)
		else:
			paramtype = ["Unit"]
		dic={}
		dic['type'] = 'function'
		dic['name']=p[1].value
		SCOPE.name = p[1].place
		dic['returntype']=p[6].type
		dic['paramtype'] = paramtype
		dic['place'] = p[1].place
		dic['tid'] = SCOPE.getid()
		if p[3].place == None:
			dic['lenarg'] = 0
		else:
			dic['lenarg'] = len(p[3].place)
		getscope(SCOPE.pid).addentry(dic)

		p[0] = Node("method_header", [p[1], p[2], p[3], child2, child3, p[6], child4])

def p_func_arg_start(p):
		'''func_arg_start : LPAREN'''
		global SCOPE
		global CSCOPE

		CSCOPE = Env(SCOPE,objecttype = 'function')
		SCOPE = CSCOPE
		child1 = create_leaf("LPAREN", p[1])
		p[0] = Node("func_args_start", [child1])

def p_fun_params_opt(p):
	'''fun_params_opt : fun_params
					| empty'''
	p[0] = Node("fun_params_opt",[p[1]])
	p[0].place = p[1].place
	p[0].type = p[1].type

def p_fun_params(p):
	'''fun_params : fun_variable_declarator_id
				  | fun_params COMMA fun_variable_declarator_id'''
	if len(p)==2:
		p[0] = Node("fun_params",[p[1]])
		p[0].place = [p[1].place]
		p[0].type = [p[1].type]
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("fun_params",[p[1],child1,p[3]])
		p[0].place = p[1].place + [p[3].place]
		p[0].type = p[1].type + [p[3].type]


def p_method_return_type(p):
		'''method_return_type : type'''
		p[0] = Node("method_return_type", [p[1]])
		p[0].type = p[1].type

def p_method_return_type1(p):
		'''method_return_type : TYPE_VOID'''
		child1 = create_leaf("VOID", p[1])
		p[0] = Node("method_return_type", [child1])
		p[0].type = "Unit"
def p_method_header_name(p):
		'''method_header_name : KEYWORD_DEF IDENTIFIER'''
		child1 = create_leaf("DEF", p[1])
		child2 = create_leaf("IDENTIFIER", p[2])

		if p[2] == 'main':
			funbegin = 'main'
		else:
			funbegin = newlabel()

		emit(['label', funbegin])
		p[0] = Node("method_header_name", [child1, child2],place=funbegin,value = p[2])


def p_method_body(p):
		'''method_body : method_start_scope block_statements_opt end_scope '''
		p[0] = Node("method_body", [p[1], p[2], p[3]])


def p_method_start_scope(p):
		'''method_start_scope : BLOCKBEGIN'''
		child1 = create_leaf("BLOCK_BEGIN", p[1])
		p[0] = Node("start_scope", [child1])




# # # CLASS DECLARATION
# def p_class_declaration(p):
# 	'''class_declaration : class_header class_body'''
# 	p[0] = Node("class_declaration", [p[1], p[2]])


# def p_class_header(p):
# 	'''class_header : KEYWORD_CLASS simple_name class_param_clause '''
# 	child1 = create_leaf("CLASS",p[1])
# 	p[0] = Node("class_header",[child1,p[2],p[3]])
# 	global SCOPE
# 	dic = {}
# 	dic['type'] = 'object'
# 	dic['name'] = p[2].place
# 	dic['place'] = newtemp()
# 	getscope(SCOPE.pid).addentry(dic)


# def p_class_param_clause(p):
# 	'''class_param_clause : func_arg_start class_params_opt RPAREN'''
# 	child2 = create_leaf("RPAREN",p[3])
# 	p[0] = Node("class_param_clause",[child1,p[2],child2])


# def p_class_param_opt(p):
# 	'''class_params_opt : class_params
# 						| empty '''
# 	p[0] = Node("class_param_opt",[p[1]])


# def p_class_params(p):
# 	'''class_params : class_param
# 					| class_params COMMA class_param'''
# 	if len(p)==2:
# 		p[0] = Node("class_params",[p[1]])
# 	else:
# 		child1 = create_leaf("COMMA",p[2])
# 		p[0] = Node("class_params",[p[1],child1,p[3]])


# def p_class_param(p):
# 	'''class_param : class_declaration_keyword_opt variable_declarator_id'''
# 	p[0] = Node("class_param",[p[1],p[2],p[3]])


# def p_class_declaration_keyword_opt1(p):
# 	'''class_declaration_keyword_opt : declaration_keyword'''
# 	p[0] = Node("class_declaration_keyword_opt",[p[1]])

# def p_class_declaration_keyword_opt2(p):
# 	'''class_declaration_keyword_opt : empty'''
# 	p[0] = Node("class_declaration_keyword_opt",[p[1]])

# def p_type_opt(p):
# 	'''type_opt : COLON type
# 				| empty'''
# 	if len(p)==2:
# 		p[0] = Node("type_opt",[p[1]])
# 	else:
# 		child1 = create_leaf("COLON",p[1])
# 		p[0] = Node("type_opt",[child1,p[2]])

# def p_class_body(p):
# 	'''class_body : class_body_start block_statements_opt end_scope '''

# 	p[0] = Node("class_body", [p[1], p[2], p[3]])
# 	# p[0] = Node("class_body", [p[1]])

# def p_class_body_start(p):
# 	'''class_body_start : BLOCKBEGIN'''
# 	child1 = create_leaf("BLOCK_BEGIN", p[1])
# 	p[0] = Node("class_body_start", [child1])
# 	classbegin = newlabel()
# 	emit([classbegin,": "])

#EMPTY RULE
def p_empty(p):
		'empty :'
		child1 = create_leaf("", "")
		p[0] = Node("empty", [child1])
		p[0].type = "Unit"
		pass


LEAVES = {	'KEYWORD_OBJECT',
			'KEYWORD_EXTENDS',
			'KEYWORD_PRINT',
			'KEYWORD_PRINTLN',
			'KEYWORD_SCAN',
			'IDENTIFIER',
			'BLOCKBEGIN','BLOCKEND',
			'LBRAC','RBRAC',
			'OR','AND','OR_BITWISE','AND_BITWISE','XOR','EqualityOp',
			'RelationalOp','ShiftOp','AddOp','Multop','Unary10p','UnaryOp'
			'LPAREN','RPAREN',
			'LiteralConst','IntFloatConst',
			'COMMA','ModifierKeyword',
			'KEYWORD_VAR/VAL','OVERRIDE'
			'STATE_END','FUNTYPE','COLON','TYPE',
			'ARRAY','DOT',
			'NEW','MATCH','CASE',
			'INT_CONST','IF','ELSE',
			'DO','WHILE','FOR',
			'CHOOSE','UNTIL_TO','BY','RETURN',
			'CLASS','VOID','DEF','empty',
			'ASOP','ASSIGN_OP','OFDIM'
			}
