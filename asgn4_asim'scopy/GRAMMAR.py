class Node(object): 
		gid = 1   
		def __init__(self,name,children):
				self.name = name
				self.children = children
				self.id=Node.gid
				Node.gid+=1

def create_leaf(name1,name2):
		leaf1 = Node(name2,[])
		leaf2 = Node(name1,[leaf1])
		return leaf2

def p_program_structure(p):
	'''ProgramStructure : ProgramStructure  class_and_objects
										| class_and_objects '''
	if len(p) == 3:
		p[0] = Node("ProgramStructure", [p[1], p[2]])
	else:
		p[0] = Node("ProgramStructure", [p[1]])

def p_class_and_objects(p):
	'''class_and_objects : SingletonObject
						 | class_declaration'''
	p[0] = Node("class_and_objects", [p[1]])

def p_SingletonObject(p):
	'SingletonObject : ObjectDeclare block'
	p[0] = Node("SingletonObject", [p[1], p[2]])

def p_object_declare(p):
	'''ObjectDeclare : KEYWORD_OBJECT IDENTIFIER 
							| KEYWORD_OBJECT IDENTIFIER KEYWORD_EXTENDS IDENTIFIER'''
	if len(p) == 3:
		child1 = create_leaf("KEYWORD_OBJECT", p[1])
		child2 = create_leaf("IDENTIFIER", p[2])
		p[0] = Node("ObjectDeclare", [child1, child2])
	else:
		child1 = create_leaf("KEYWORD_OBJECT", p[1])
		child2 = create_leaf("IDENTIFIER", p[2])
		child3 = create_leaf("KEYWORD_EXTENDS", p[3])
		child4 = create_leaf("IDENTIFIER", p[4])
		p[0] = Node("ObjectDeclare", [child1, child2, child3, child4])

# BLOCK DEFINITION
def p_block(p):
	'''block : BLOCKBEGIN block_statements_opt BLOCKEND '''
	child1 = create_leaf("BLOCKBEGIN", p[1])
	child2 = create_leaf("BLOCKEND", p[3])
	p[0] = Node("block", [child1, p[2], child2])

def p_block_statements_opt(p):
	'''block_statements_opt : block_statements
							| empty '''
	p[0] = Node("block_statements_opt", [p[1]])

def p_block_statements(p):
	'''block_statements : block_statement
						| block_statements block_statement'''
	if len(p) == 2:
		p[0] = Node("block_statement", [p[1]])
	else:
		p[0] = Node("block_statements", [p[1], p[2]])

def p_block_statement(p):
	'''block_statement : local_variable_declaration_statement
						 | statement
						 | class_declaration
						 | SingletonObject
						 | method_declaration'''
	p[0] = Node("block_statement", [p[1]])

# EXPRESSION
def p_expression(p):
	'''expression : assignment_expression'''
	p[0] = Node("expression", [p[1]])

def p_expression_optional(p):
	'''expression_optional : expression
						   | empty'''
	p[0] = Node("expression_optional", [p[1]])

def p_assignment_expression(p):
		'''assignment_expression : assignment
								 | conditional_or_expression
								 | if_else_expression '''
		p[0] = Node("assignment_expression", [p[1]])

def p_if_else_expression(p):
	'''if_else_expression : KEYWORD_IF LPAREN expression RPAREN expression KEYWORD_ELSE expression'''
	child1 = create_leaf("IF",p[1])
	child2 = create_leaf("LPAREN",p[2])
	child3 = create_leaf("RPAREN",p[4])
	child4 = create_leaf("ELSE",p[6])
	p[0] = Node("if_else_expression",[child1,child2,p[3],child3,p[5],child4,p[7]])

# ASSIGNMENT
def p_assignment(p):
		'''assignment : valid_variable assignment_operator assignment_expression'''
		p[0] = Node("assignment", [p[1], p[2], p[3]])

def p_valid_variable(p):
		'''valid_variable : name
						  | array_access'''
		p[0] = Node("valid_variable", [p[1]])

def p_array_access(p):
		'''array_access : name dimension'''
		p[0] = Node("array_access", [p[1], p[2]])

def p_dimension(p):
	'''dimension : dimension LBRAC expression RBRAC
				 | LBRAC expression RBRAC '''
	if len(p)==5 :
		child1 = create_leaf("LBRAC",p[2])
		child2 = create_leaf("RBRAC",p[4])
		p[0] = Node("dimension",[p[1],child1,p[3],child2])
	else:
		child1 = create_leaf("LBRAC",p[1])
		child2 = create_leaf("RBRAC",p[3])
		p[0] = Node("dimension",[child1,p[2],child2]) 

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
		p[0] = Node("assignment_operator", [child1])        


# OR(||) has least precedence, and OR is left assosiative 
# a||b||c => first evaluate a||b then (a||b)||c
def p_conditional_or_expression(p):
		'''conditional_or_expression : conditional_and_expression
									 | conditional_or_expression OR conditional_and_expression'''
		if len(p) == 2:
			p[0] = Node("conditional_or_expression", [p[1]])
		else:
			child1 = create_leaf("OR", p[2])
			p[0] = Node("conditional_or_expression", [p[1], child1, p[3]])

# AND(&&) has next least precedence, and AND is left assosiative 
# a&&b&&c => first evalutae a&&b then (a&&b)&&c

def p_conditional_and_expression(p):
		'''conditional_and_expression : inclusive_or_expression
									  | conditional_and_expression AND inclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node("conditional_and_expression", [p[1]])
		else:
			child1 = create_leaf("AND", p[2])
			p[0] = Node("conditional_and_expression", [p[1], child1, p[3]])

def p_inclusive_or_expression(p):
		'''inclusive_or_expression : exclusive_or_expression
								   | inclusive_or_expression OR_BITWISE exclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node("inclusive_or_expression", [p[1]])
		else:
			child1 = create_leaf("OR_BITWISE", p[2])
			p[0] = Node("inclusive_or_expression", [p[1], child1, p[3]])

def p_exclusive_or_expression(p):
		'''exclusive_or_expression : and_expression
								   | exclusive_or_expression XOR and_expression'''
		if len(p) == 2:
			p[0] = Node("exclusive_or_expression", [p[1]])
		else:
			child1 = create_leaf("XOR", p[2])
			p[0] = Node("exclusive_or_expression", [p[1], child1, p[3]])

def p_and_expression(p):
		'''and_expression : equality_expression
						  | and_expression AND_BITWISE equality_expression'''
		if len(p) == 2:
			p[0] = Node("and_expression", [p[1]])
		else:
			child1 = create_leaf("AND_BITWISE", p[2])
			p[0] = Node("and_expression", [p[1], child1, p[3]])

def p_equality_expression(p):
		'''equality_expression : relational_expression
								| equality_expression EQUAL relational_expression
								| equality_expression NEQUAL relational_expression'''
		if len(p) == 2:
			p[0] = Node("relational_expression", [p[1]])
		else:
			child1 = create_leaf("EqualityOp", p[2])
			p[0] = Node("relational_expression", [p[1], child1, p[3]])
	 

def p_relational_expression(p):
		'''relational_expression : shift_expression
								 | relational_expression GREATER shift_expression
								 | relational_expression LESS shift_expression
								 | relational_expression GEQ shift_expression
								 | relational_expression LEQ shift_expression'''
		if len(p) == 2:
			p[0] = Node("relational_expression", [p[1]])
		else:
			child1 = create_leaf("RelationalOp", p[2])
			p[0] = Node("relational_expression", [p[1], child1, p[3]])
	 

def p_shift_expression(p):
				'''shift_expression : additive_expression
									| shift_expression LSHIFT additive_expression
									| shift_expression RSHIFT additive_expression'''
				if len(p) == 2:
					p[0] = Node("shift_expression", [p[1]])
				else:
					child1 = create_leaf("ShiftOp", p[2])
					p[0] = Node("shift_expression", [p[1], child1, p[3]])
			 

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


def p_unary_expression_not_plus_minus(p):
		'''unary_expression_not_plus_minus : base_variable_set
											 | TILDA unary_expression
											 | NOT unary_expression
											 | cast_expression'''
		if len(p) == 2:
			p[0] = Node("unary_expression_not_plus_minus", [p[1]])
		else:
			child1 = create_leaf("Unary_1Op", p[1])
			p[0] = Node("unary_expression_not_plus_minus", [child1, p[2]])
		

def p_base_variable_set(p):
	'''base_variable_set : variable_literal
						 | LPAREN expression RPAREN'''
	if len(p) == 2:
		p[0] = Node("base_variable_set", [p[1]])
	else:
		child1 = create_leaf("LPAREN", p[1])
		child2 = create_leaf("RPAREN", p[3])
		p[0] = Node("base_variable_set", [child1, p[2], child2])

def p_variableliteral(p):
		'''variable_literal : valid_variable
							| primary'''
		p[0] = Node("variable_literal", [p[1]])


def p_cast_expression(p):
				'''cast_expression : LPAREN primitive_type RPAREN unary_expression'''
				child1 = create_leaf("LPAREN", p[1])
				child2 = create_leaf("RPAREN", p[3])
				p[0] = Node("cast_expression", [child1, p[2], child2, p[4]])

def p_primary(p):
		'''primary : literal
					| method_invocation'''
		p[0] = Node("primary", [p[1]])

def p_literal(p):
		'''literal : int_float
					| c_literal ''' 
		p[0] = Node("literal", [p[1]])

def p_c_literal(p):
		'''c_literal : CHAR
					| STRING
					| BOOL_CONSTT
					| BOOL_CONSTF
					| KEYWORD_NULL'''
		child1 = create_leaf("LiteralConst",[p[1]])
		p[0] = Node("c_literal", [child1])

def p_int_float(p):
		'''int_float : DOUBLE_NUMBER
					 | INT_NUMBER '''
		child1 = create_leaf("IntFloatConst", p[1])
		p[0] = Node("int_float", [child1])


# FUNCTION CALL
def p_method_invocation(p):
		'''method_invocation : name LPAREN argument_list_opt RPAREN '''
		child1 = create_leaf("LPAREN", p[2])
		child2 = create_leaf("RPAREN", p[4])
		p[0] = Node("method_invocation", [p[1], child1, p[3], child2])

def p_argument_list_opt(p):
		'''argument_list_opt : argument_list'''
		p[0] = Node("argument_list_opt", [p[1]])

def p_argument_list_opt2(p):
		'''argument_list_opt : empty'''
		p[0] = Node("argument_list_opt", [p[1]])

def p_argument_list(p):
		'''argument_list : expression
						| argument_list COMMA expression'''
		if len(p) == 2:
			p[0] = Node("argument_list", [p[1]])
		else:
			child1 = create_leaf("COMMA", p[2])
			p[0] = Node("argument_list", [p[1], child1, p[3]])


# LOCAL VARIABLE DECLARATION

def p_modifier(p):
			'''modifier : KEYWORD_PROTECTED
						| KEYWORD_PRIVATE'''
			child1 = create_leaf("ModifierKeyword", p[1])
			p[0] = Node("modifier", [child1])

def p_modifier_opts(p):
	'''modifier_opts : modifier
					 | empty '''
	p[0] = Node("modifier_opts", [p[1]])

def p_declaration_keyword(p):
	'''declaration_keyword : KEYWORD_VAR
						   | KEYWORD_VAL '''
	child1 = create_leaf("KEYWORD_VAR/VAL", p[1])
	p[0] = Node("declaration_keyword", [child1])


def p_local_variable_declaration_statement(p):
			'''local_variable_declaration_statement : local_variable_declaration TERMINATOR '''
			child1 = create_leaf("STATE_END", p[2])
			p[0] = Node("local_variable_declaration_statement", [p[1], child1])

def p_local_variable_declaration(p):
			'''local_variable_declaration : modifier_opts declaration_keyword variable_declaration_body'''
			p[0] = Node("local_variable_declaration", [p[1], p[2], p[3]])

def p_variable_declaration_initializer(p):
	'''variable_declaration_initializer : expression
										| array_initializer
			                            | class_initializer'''
	p[0] = Node("variable_declaration_initializer", [p[1]])

def p_variable_argument_list(p):
	''' variable_argument_list : variable_declaration_initializer
										| variable_argument_list COMMA variable_declaration_initializer'''
	if len(p) == 2:
		p[0] = Node("variable_argument_list", [p[1]])
	else:
		child1 = create_leaf("COMMA", p[2])
		p[0] = Node("variable_argument_list", [p[1], child1, p[3]])

def p_variable_declaration_body_1(p): # eg. var x:Int = 2; or var x = 2 or var x,y,z:Int = 2 or var x,y,z = 2;
	'''variable_declaration_body : identifiers type_opt ASOP  variable_declaration_initializer '''
	child1 = create_leaf("ASOP", p[3])
	p[0] = Node("variable_declaration_body", [p[1], p[2], child1, p[4]])

def p_identifiers(p):
	''' identifiers : identifiers COMMA IDENTIFIER 
					| IDENTIFIER'''
	if len(p)==2:
		child1 = create_leaf("IDENTIFIER",p[1])
		p[0] = Node("identifiers",[child1])
	else:
		child1 = create_leaf("COMMA",p[2])
		child2 = create_leaf("IDENTIFIER",p[3])
		p[0] = Node("identifiers",[p[1],child1,child2])



def p_variable_declaration_body_2(p): # eg. var (x:Int,y:Array[String],z) = (2,new Array[String](5),3);
	'''variable_declaration_body : LPAREN variable_list RPAREN ASOP LPAREN variable_argument_list RPAREN'''	
	child1 = create_leaf("LPAREN", p[1])
	child2 = create_leaf("RPAREN", p[3])
	child3 = create_leaf("ASOP", p[4])
	child4 = create_leaf("LPAREN", p[5])
	child5 = create_leaf("RPAREN", p[7])
	p[0] = Node("variable_declaration_body", [child1, p[2], child2, child3, child4, p[6], child5])

def p_variable_list(p):					# eg. x,y:Int,z
	''' variable_list : variable_dec 
					  | variable_list COMMA variable_dec'''
	if len(p)==2:
		p[0] = Node("variable_list",[p[1]])
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("variable_list",[p[1],child1,p[3]])

def p_variable_dec(p):						# eg. x:Int or x
	''' variable_dec : IDENTIFIER type_opt'''
	child1 = create_leaf("IDENTIFIER",p[1])
	p[0] = Node("variable_dec",[child1,p[2]])

# def p_variable_declaration_body_3(p): # eg. var x,y,z = (a:Int) => a*a;  Notice, x,y,z are functions.
# 	''' variable_declaration_body : identifiers ASOP LPAREN fun_params RPAREN FUNTYPE expression'''      

# 	child2 = create_leaf("ASOP", p[2])
# 	child3 = create_leaf("LPAREN", p[3])
# 	child4 = create_leaf("RPAREN", p[5])
# 	child5 = create_leaf("FUNTYPE", p[6])
# 	p[0] = Node("variable_declaration_body", [p[1], child2, child3, p[4], child4, child5,p[7]])


def p_expr_opt(p):
	''' expr_opt : ASOP variable_declaration_initializer 
				 | empty '''
	if len(p) > 2:
		child1 = create_leaf("ASOP",p[1])
		p[0] = Node("expr_opt",[child1,p[2]])
	else:
		p[0] = Node("expr_opt",[p[1]])


def p_variable_declarator_id(p):
	'''variable_declarator_id : IDENTIFIER COLON type'''
	child1 = create_leaf("IDENTIFIER", p[1])
	child2 = create_leaf("COLON", p[2])
	p[0] = Node("variable_declarator_id", [child1, child2, p[3]])


#DATA_TYPES AND VARIABLE_TYPES
def p_type(p):
	'''type : primitive_type 
			| reference_type '''
	p[0] = Node("type", [p[1]])

def p_primitive_type(p):
	'''primitive_type : TYPE_INT
						| TYPE_DOUBLE
						| TYPE_CHAR
						| TYPE_STRING
						| TYPE_BOOLEAN 
						| TYPE_VOID   '''
	child1 = create_leaf("TYPE", p[1])
	p[0] = Node("primitive_type", [child1]) 


def p_reference_type(p):
	'''reference_type : class_data_type
					  | array_data_type'''
	p[0] = Node("reference_type", [p[1]])

def p_class_data_type(p):
	'''class_data_type : name'''
	p[0] = Node("class_data_type", [p[1]])

def p_array_data_type(p):
	'''array_data_type : KEYWORD_ARRAY LBRAC type RBRAC'''
	child1 = create_leaf("ARRAY", p[1])
	child2 = create_leaf("LBRAC", p[2])
	child3 = create_leaf("RBRAC", p[4])
	p[0] = Node("array_data_type", [child1, child2, p[3], child3])


#VARIABLE_NAMES
def p_name(p):
		'''name : simple_name
				| qualified_name'''
		p[0] = Node("name", [p[1]])


def p_simple_name(p):
		'''simple_name : IDENTIFIER'''
		child1 = create_leaf("IDENTIFIER", p[1])
		p[0] = Node("simple_name", [child1])


def p_qualified_name(p):
		'''qualified_name : name INST simple_name'''
		child1 = create_leaf("DOT", p[2])
		p[0] = Node("qualified_name", [p[1], child1, p[3]])


#INITIALIZERS
def p_array_initializer(p):
	''' array_initializer : KEYWORD_NEW KEYWORD_ARRAY LBRAC type RBRAC LPAREN conditional_or_expression RPAREN
												| KEYWORD_ARRAY LPAREN argument_list_opt RPAREN
												| KEYWORD_ARRAY LBRAC type RBRAC LPAREN argument_list_opt RPAREN
												| multidimensional_array_initializer'''
	if len(p) == 9:
		child1 = create_leaf("NEW", p[1])
		child2 = create_leaf("ARRAY", p[2])
		child3 = create_leaf("LBRAC", p[3])
		child4 = create_leaf("RBRAC", p[5])
		child5 = create_leaf("LPAREN", p[6])
		child7 = create_leaf("RPAREN", p[8])

		p[0] = Node("array_initializer", [child1, child2, child3, p[4], child4, child5, p[6], child7])
	
	elif len(p)==8:
		child2 = create_leaf("ARRAY", p[1])
		child3 = create_leaf("LBRAC", p[2])
		child4 = create_leaf("RBRAC", p[4])
		child5 = create_leaf("LPAREN", p[5])
		child7 = create_leaf("RPAREN", p[7])

		p[0] = Node("array_initializer", [child2, child3, p[3], child4, p[5],child7])		
	
	elif len(p) ==2:
		p[0] = Node("array_initializer",[p[1]])

	else:
		child1 = create_leaf("ARRAY", p[1])
		child2 = create_leaf("LPAREN", p[2])
		child3 = create_leaf("RPAREN", p[4]) 
		p[0] = Node("array_initializer", [child1, child2, p[3], child3])   

def p_multidimensional_array_initializer(p):
	''' multidimensional_array_initializer : KEYWORD_ARRAY INST KEYWORD_OFDIM LBRAC type RBRAC LPAREN argument_list RPAREN'''
	child1 = create_leaf("ARRAY",p[1])
	child2 = create_leaf("DOT",p[2])
	child3 = create_leaf("OFDIM",p[3])
	child4 = create_leaf("LBRAC",p[4])
	child5 = create_leaf("RBRAC",p[6])
	child6 = create_leaf("LPAREN",p[7])
	child7 = create_leaf("RPAREN",p[9])
	p[0] = Node("multidimensional_array_initializer",[child1,child2,child3,child4,p[5],child5,child6,p[8],child7])

def p_class_initializer(p):
	''' class_initializer : KEYWORD_NEW name LPAREN argument_list_opt RPAREN ''' 
	child1 = create_leaf("NEW", p[1])
	child2 = create_leaf("LPAREN", p[3])
	child3 = create_leaf("RPAREN", p[5])
	p[0] = Node("class_initializer", [child1, p[2], child2, p[4], child3])

# STATEMENTS
def p_statement(p):
        '''statement : normal_statement 
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | do_while_statement
                     | for_statement'''
        p[0] = Node("statement", [p[1]])

def p_normal_statement(p):
	'''normal_statement : block 
						| expression_statement
						| empty_statement
						| return_statement'''

	p[0] = Node("normal_statement", [p[1]])
 
def p_expression_statement(p):
	'''expression_statement : statement_expression TERMINATOR'''
	child1 = create_leaf("STATE_END", p[2])
	p[0] = Node("expression_statement", [p[1], child1])
															 

def p_statement_expression(p):
	'''statement_expression : assignment
							| method_invocation'''
			
	p[0] = Node("statement_expression", [p[1]])
		
	
#IF THEN STATEMENT
def p_if_then_statement(p):
	'''if_then_statement : KEYWORD_IF LPAREN expression RPAREN statement'''
	child1 = create_leaf("IF",p[1])
	child2 = create_leaf("LPAREN",p[2])
	child3 = create_leaf("RPAREN",p[4])
	p[0] = Node("if_then_statement",[child1,child2,p[3],child3,p[5]])

def p_if_then_else_statement(p):
        '''if_then_else_statement : KEYWORD_IF LPAREN expression RPAREN if_then_else_intermediate KEYWORD_ELSE statement'''
        child1 = create_leaf("IF", p[1])
        child2 = create_leaf("LPAREN", p[2])
        child3 = create_leaf("RPAREN", p[4])
        child4 = create_leaf("ELSE", p[6])
        p[0] = Node("if_then_else_statement", [child1, child2, p[3], child3, p[5], child4, p[7]])
       

def p_if_then_else_statement_precedence(p):
        '''if_then_else_statement_precedence : KEYWORD_IF LPAREN expression RPAREN if_then_else_intermediate KEYWORD_ELSE if_then_else_intermediate'''
        child1 = create_leaf("IF", p[1])
        child2 = create_leaf("LPAREN", p[2])
        child3 = create_leaf("RPAREN", p[4])
        child4 = create_leaf("ELSE", p[6])
        p[0] = Node("if_then_else_statement_precedence", [child1, child2, p[3], child3, p[5], child4, p[7]])
      

def p_if_then_else_intermediate(p):
        '''if_then_else_intermediate : normal_statement
                                     | if_then_else_statement_precedence'''
        p[0] = Node("if_then_else_intermediate", [p[1]]) 		 

# WHILE_LOOP
def p_while_statement(p):
	'''while_statement : KEYWORD_WHILE LPAREN expression RPAREN statement'''
	child1 = create_leaf("WHILE", p[1])
	child2 = create_leaf("LPAREN", p[2])
	child3 = create_leaf("RPAREN", p[4])
	p[0] = Node("while_statement", [child1, child2, p[3], child3, p[5]])
	
#DO_WHILE_LOOP
def p_do_while_statement(p):
	'''do_while_statement : KEYWORD_DO statement KEYWORD_WHILE LPAREN expression RPAREN TERMINATOR '''
	child1 = create_leaf("DO", p[1])
	child2 = create_leaf("WHILE", p[3])
	child3 = create_leaf("LPAREN", p[4])
	child4 = create_leaf("RPAREN", p[6])
	child5 = create_leaf("STATE_END", p[7])
	p[0] = Node("do_while_statement", [child1, p[2], child2, child3, p[5], child4, child5])
			 
# FOR_LOOP
def p_for_statement1(p):
	'''for_statement : KEYWORD_FOR LPAREN for_logic RPAREN statement'''
	child1 = create_leaf ("FOR",p[1])
	child2 = create_leaf ("LPAREN",p[2])
	child3 = create_leaf ("RPAREN",p[4])
	p[0] = Node("for_statement",[child1,child2,p[3],child3,p[5]])

def p_for_statement2(p):
	'''for_statement : KEYWORD_FOR BLOCKBEGIN for_logic BLOCKEND statement'''
	child1 = create_leaf ("FOR",p[1])
	child2 = create_leaf ("BLOCKBEGIN",p[2])
	child3 = create_leaf ("BLOCKEND",p[4])
	p[0] = Node("for_statement",[child1,child2,p[3],child3,p[5]])

def p_for_logic(p):
		''' for_logic : for_update 
									| for_update TERMINATOR for_logic '''
		if len(p)==2:
			p[0]=Node("for_logic",[p[1]])
		else:
			child1 = create_leaf("STATE_END",p[2])
			p[0] = Node("for_logic",[p[1],child1,p[3]])

def p_for_update(p):
	''' for_update : for_loop for_step_opts '''
	p[0]=Node("for_update",[p[1],p[2]])

def p_for_loop(p):
	''' for_loop : IDENTIFIER CHOOSE expression for_untilTo expression '''
	
	child1 = create_leaf("IDENTIFIER",p[1])
	child2 = create_leaf("CHOOSE",p[2])
	p[0] = Node("for_loop_st",[child1,child2,p[3],p[4],p[5]])

def p_for_untilTo(p):
	'''for_untilTo : KEYWORD_UNTIL 
									| KEYWORD_TO'''

	child1 = create_leaf("UNTIL_TO",p[1])
	p[0]=Node("for_untilTo",[child1])


def p_for_step_opts(p):
	''' for_step_opts : KEYWORD_BY expression
										| empty'''
	if len(p)==2:
		p[0]=Node("for_step_opts",[p[1]])
	else :
		child1 = create_leaf("BY",p[1])
		p[0]=Node("for_step_opts",[child1,p[2]])

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



# CLASS DECLARATION
def p_class_declaration(p):
	'''class_declaration : class_header class_body'''
	p[0] = Node("class_declaration", [p[1], p[2]])

def p_class_header(p):
	'''class_header : KEYWORD_CLASS simple_name modifier_opts class_param_clause_opt class_template_opt'''
	child1 = create_leaf("CLASS",p[1])
	p[0] = Node("class_header",[child1,p[2],p[3],p[4],p[5]])

def p_class_param_clause_opt(p):
	'''class_param_clause_opt : class_param_clause 
							  | empty'''
	p[0] = Node("class_param_clause_opt",[p[1]])

def p_class_param_clause(p):
	'''class_param_clause : LPAREN class_params_opt RPAREN'''
	child1 = create_leaf("LPAREN",p[1])
	child2 = create_leaf("RPAREN",p[3])
	p[0] = Node("class_param_clause",[child1,p[2],child2])

def p_class_param_opt(p):
	'''class_params_opt : class_params
					 	| empty '''
	p[0] = Node("class_param_opt",[p[1]])

def p_class_params(p):
	'''class_params : class_param
					| class_params COMMA class_param'''
	if len(p)==2:
		p[0] = Node("class_params",[p[1]])
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("class_params",[p[1],child1,p[3]])

def p_class_param(p):
	'''class_param : class_declaration_keyword_opt variable_declarator_id expr_opt'''
	p[0] = Node("class_param",[p[1],p[2],p[3]])

def p_override_opt(p):
	'''override_opt : override
					 | empty'''
	p[0] = Node("override_opt",[p[1]])

def p_override(p):
	'''override : KEYWORD_OVERRIDE'''
	child1 = create_leaf("OVERRIDE",p[1])
	p[0] = Node("override",[child1])

def p_class_declaration_keyword_opt(p):
	'''class_declaration_keyword_opt : override_opt modifier_opts declaration_keyword 
									 | empty '''
	if len(p)==4:
		p[0] = Node("class_declaration_keyword_opt",[p[1],p[2],p[3]])
	else:
		p[0] = Node("class_declaration_keyword_opt",[p[1]])

def p_type_opt(p):
	'''type_opt : COLON type 
				| empty'''
	if len(p)==2:
		p[0] = Node("type_opt",[p[1]])
	else:
		child1 = create_leaf("COLON",p[1])
		p[0] = Node("type_opt",[child1,p[2]])

def p_class_template_opt(p):
	'''class_template_opt : class_template 
						  | empty '''
	p[0] = Node("class_template_opt",[p[1]])


def p_class_template(p):
	'''class_template : KEYWORD_EXTENDS simple_name LPAREN variable_list RPAREN'''
	child1 = create_leaf("KEYWORD_EXTENDS", p[1])
	child2 = create_leaf("LPAREN", p[3])
	child3 = create_leaf("RPAREN", p[5])
	p[0] = Node("class_header_extends", [child1, p[2], child2, p[4], child3])

def p_class_body(p):
	'''class_body : block ''' 
	p[0] = Node("class_body", [p[1]])


#METHOD DECLARATION
def p_method_declaration1(p):
	'''method_declaration : method_header method_body'''
	p[0] = Node("method_declaration", [p[1], p[2]])

# def p_method_declaration2(p):
# 	'''method_declaration : KEYWORD_DEF fun_sig block'''
# 	child1 = create_leaf("DEF",p[1])
# 	p[0] = Node("method_declaration",[child1,p[2],p[3]])

def p_method_header(p):
	'''method_header : KEYWORD_DEF fun_def'''
	child1 = create_leaf("DEF",p[1])
	p[0] = Node("method_header",[child1,p[2]])

def p_fun_def1(p):
	'''fun_def : fun_sig type_opt ASOP'''
	child1 = create_leaf("ASOP",p[3])
	p[0] = Node("fun_def",[p[1],p[2],child1])

def p_fun_def2(p):
	'''fun_def : fun_sig type_opt'''
	# child1 = create_leaf("ASOP",p[3])
	p[0] = Node("fun_def",[p[1],p[2]])

def p_fun_sig(p):
	'''fun_sig : simple_name fun_param_clause'''
	p[0] = Node("fun_sig",[p[1],p[2]])

# def p_fun_param_clause_opt(p):
# 	'''fun_param_clause_opt : fun_param_clause
# 							| empty'''
# 	p[0] = Node("fun_param_clause_opt",[p[1]])

def p_fun_param_clause(p):
	'''fun_param_clause : LPAREN fun_params_opt RPAREN  '''
	child1 = create_leaf("LPAREN",p[1])
	child2 = create_leaf("RPAREN",p[3])
	p[0] = Node("fun_param_clause",[child1,p[2],child2])

def p_fun_params_opt(p):
	'''fun_params_opt : fun_params
					| empty'''
	p[0] = Node("fun_params_opt",[p[1]])

def p_fun_params(p):
	'''fun_params : fun_param 
				  | fun_params COMMA fun_param'''
	if len(p)==2:
		p[0] = Node("fun_params",[p[1]])
	else:
		child1 = create_leaf("COMMA",p[2])
		p[0] = Node("fun_params",[p[1],child1,p[3]])

def p_fun_param(p):
	'''fun_param : variable_declarator_id expr_opt'''
	p[0] = Node("fun_param",[p[1],p[2]])

def p_method_body(p):
	'''method_body : block 
					| variable_declaration_initializer''' 
	p[0] = Node("method_body", [p[1]])


#EMPTY RULE
def p_empty(p):
		'empty :'
		child1 = create_leaf("", "")
		p[0] = Node("empty", [child1])
		pass


LEAVES = {	'KEYWORD_OBJECT',
			'KEYWORD_EXTENDS',				
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
			'NEW',
			'INT_CONST','IF','ELSE',
			'DO','WHILE','FOR',
			'CHOOSE','UNTIL_TO','BY','RETURN',
			'CLASS','VOID','DEF','empty',
			'ASOP','ASSIGN_OP','OFDIM'
			}