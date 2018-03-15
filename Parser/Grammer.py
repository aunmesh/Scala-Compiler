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

		leaf1 = leaf_gen(Dict["ASSIGN_OP"], p[1])
		p[0] = Node(Dict["assignment_operator"], [leaf1])  



# OR(||) has least precedence, and OR is left assosiative 
# a||b||c => first evaluate a||b then (a||b)||c
def p_conditional_or_expression(p):
		'''conditional_or_expression : conditional_and_expression
									 | conditional_or_expression OR conditional_and_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["conditional_or_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["OR"], p[2])
			p[0] = Node(Dict["conditional_or_expression"], [p[1], leaf1, p[3]])

# AND(&&) has next least precedence, and AND is left assosiative 
# a&&b&&c => first evalutae a&&b then (a&&b)&&c

def p_conditional_and_expression(p):
		'''conditional_and_expression : inclusive_or_expression
									  | conditional_and_expression AND inclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["conditional_and_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["AND"], p[2])
			p[0] = Node(Dict["conditional_and_expression"], [p[1], leaf1, p[3]])

def p_inclusive_or_expression(p):
		'''inclusive_or_expression : exclusive_or_expression
								   | inclusive_or_expression OR_BITWISE exclusive_or_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["inclusive_or_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["OR_BITWISE"], p[2])
			p[0] = Node(Dict["inclusive_or_expression"], [p[1], leaf1, p[3]])

def p_exclusive_or_expression(p):
		'''exclusive_or_expression : and_expression
								   | exclusive_or_expression XOR and_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["exclusive_or_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["XOR"], p[2])
			p[0] = Node(Dict["exclusive_or_expression"], [p[1], leaf1, p[3]])


def p_and_expression(p):
		'''and_expression : equality_expression
						  | and_expression AND_BITWISE equality_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["and_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["AND_BITWISE"], p[2])
			p[0] = Node(Dict["and_expression"], [p[1], leaf1, p[3]])

def p_equality_expression(p):
		'''equality_expression : relational_expression
								| equality_expression EQUAL relational_expression
								| equality_expression NEQUAL relational_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["relational_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["EqualityOp"], p[2])
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
			leaf1 = leaf_gen(Dict["RelationalOp"], p[2])
			p[0] = Node(Dict["relational_expression"], [p[1], leaf1, p[3]])
	 

def p_shift_expression(p):
				'''shift_expression : additive_expression
									| shift_expression LSHIFT additive_expression
									| shift_expression RSHIFT additive_expression'''
				if len(p) == 2:
					p[0] = Node(Dict["shift_expression"], [p[1]])
				else:
					leaf1 = leaf_gen(Dict["ShiftOp"], p[2])
					p[0] = Node(Dict["shift_expression"], [p[1], leaf1, p[3]])




def p_additive_expression(p):
		'''additive_expression : multiplicative_expression
								 | additive_expression PLUS multiplicative_expression
								 | additive_expression MINUS multiplicative_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["additive_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["AddOp"], p[2])
			p[0] = Node(Dict["additive_expression"], [p[1], leaf1, p[3]])

def p_multiplicative_expression(p):
		'''multiplicative_expression : unary_expression
									 | multiplicative_expression TIMES unary_expression
									 | multiplicative_expression DIVIDE unary_expression
									 | multiplicative_expression REMAINDER unary_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["multiplicative_expression"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["MultOp"], p[2])
			p[0] = Node(Dict["multiplicative_expression"], [p[1], leaf1, p[3]])

def p_unary_expression(p):
		'''unary_expression : PLUS unary_expression
							| MINUS unary_expression
							| unary_expression_not_plus_minus'''
		if len(p) == 3:
			leaf1 = leaf_gen(Dict["UnaryOp"],p[1])
			p[0] = Node(Dict["unary_expression"], [leaf1, p[2]])
		else:
			p[0] = Node(Dict["unary_expression"], [p[1]])




def p_unary_expression_not_plus_minus(p):
		'''unary_expression_not_plus_minus : base_variable_set
											 | TILDA unary_expression
											 | NOT unary_expression
											 | cast_expression'''
		if len(p) == 2:
			p[0] = Node(Dict["unary_expression_not_plus_minus"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["Unary_1Op"], p[1])
			p[0] = Node(Dict["unary_expression_not_plus_minus"], [leaf1, p[2]])
		

def p_base_variable_set(p):
	'''base_variable_set : variable_literal
						 | LPAREN expression RPAREN'''
	if len(p) == 2:
		p[0] = Node(Dict["base_variable_set"], [p[1]])
	else:
		leaf1 = leaf_gen(Dict["LPAREN"], p[1])
		leaf2 = leaf_gen(Dict["RPAREN"], p[3])
		p[0] = Node(Dict["base_variable_set"], [leaf1, p[2], leaf2])

def p_variableliteral(p):
		'''variable_literal : valid_variable
							| primary'''
		p[0] = Node(Dict["variable_literal"], [p[1]])


def p_cast_expression(p):
				'''cast_expression : LPAREN primitive_type RPAREN unary_expression'''
				leaf1 = leaf_gen(Dict["LPAREN"], p[1])
				leaf2 = leaf_gen(Dict["RPAREN"], p[3])
				p[0] = Node(Dict["cast_expression"], [leaf1, p[2], leaf2, p[4]])




def p_primary(p):
		'''primary : literal
					| method_invocation'''
		p[0] = Node(Dict["primary"], [p[1]])

def p_literal(p):
		'''literal : int_float
					| c_literal ''' 
		p[0] = Node(Dict["literal"], [p[1]])

def p_c_literal(p):
		'''c_literal : CHAR
					| STRING
					| BOOL_CONSTT
					| BOOL_CONSTF
					| KEYWORD_NULL'''
		leaf1 = leaf_gen(Dict["LiteralConst"],[p[1]])
		p[0] = Node(Dict["c_literal"], [leaf1])


def p_int_float(p):
		'''int_float : DOUBLE_NUMBER
					 | INT_NUMBER '''
		leaf1 = leaf_gen(Dict["IntFloatConst"], p[1])
		p[0] = Node(Dict["int_float"], [leaf1])


# FUNCTION CALL
def p_method_invocation(p):
		'''method_invocation : name LPAREN argument_list_opt RPAREN '''
		leaf1 = leaf_gen(Dict["LPAREN"], p[2])
		leaf2 = leaf_gen(Dict["RPAREN"], p[4])
		p[0] = Node(Dict["method_invocation"], [p[1], leaf1, p[3], leaf2])

def p_argument_list_opt(p):
		'''argument_list_opt : argument_list'''
		p[0] = Node(Dict["argument_list_opt"], [p[1]])

def p_argument_list_opt2(p):
		'''argument_list_opt : empty'''
		p[0] = Node(Dict["argument_list_opt"], [p[1]])

def p_argument_list(p):
		'''argument_list : expression
						| argument_list COMMA expression'''
		if len(p) == 2:
			p[0] = Node(Dict["argument_list"], [p[1]])
		else:
			leaf1 = leaf_gen(Dict["COMMA"], p[2])
			p[0] = Node(Dict["argument_list"], [p[1], leaf1, p[3]])



# LOCAL VARIABLE DECLARATION

def p_modifier(p):
			'''modifier : KEYWORD_PROTECTED
						| KEYWORD_PRIVATE'''
			leaf1 = leaf_gen(Dict["ModifierKeyword"], p[1])
			p[0] = Node(Dict["modifier"], [leaf1])

def p_modifier_opts(p):
	'''modifier_opts : modifier
					 | empty '''
	p[0] = Node(Dict["modifier_opts"], [p[1]])

def p_declaration_keyword(p):
	'''declaration_keyword : KEYWORD_VAR
						   | KEYWORD_VAL '''
	leaf1 = leaf_gen(Dict["KEYWORD_VAR/VAL"], p[1])
	p[0] = Node(Dict["declaration_keyword"], [leaf1])


def p_local_variable_declaration_statement(p):
			'''local_variable_declaration_statement : local_variable_declaration TERMINATOR '''
			leaf1 = leaf_gen(Dict["STATE_END"], p[2])
			p[0] = Node(Dict["local_variable_declaration_statement"], [p[1], leaf1])

def p_local_variable_declaration(p):
			'''local_variable_declaration : modifier_opts declaration_keyword variable_declaration_body'''
			p[0] = Node(Dict["local_variable_declaration"], [p[1], p[2], p[3]])

def p_variable_declaration_initializer(p):
	'''variable_declaration_initializer : expression
										| array_initializer
			                            | class_initializer'''
	p[0] = Node(Dict["variable_declaration_initializer"], [p[1]])

def p_variable_argument_list(p):
	''' variable_argument_list : variable_declaration_initializer
										| variable_argument_list COMMA variable_declaration_initializer'''
	if len(p) == 2:
		p[0] = Node(Dict["variable_argument_list"], [p[1]])
	else:
		leaf1 = leaf_gen(Dict["COMMA"], p[2])
		p[0] = Node(Dict["variable_argument_list"], [p[1], leaf1, p[3]])

def p_variable_declaration_body_1(p): # eg. var x:Int = 2; or var x = 2 or var x,y,z:Int = 2 or var x,y,z = 2;
	'''variable_declaration_body : identifiers type_opt ASOP  variable_declaration_initializer '''
	leaf1 = leaf_gen(Dict["ASOP"], p[3])
	p[0] = Node(Dict["variable_declaration_body"], [p[1], p[2], leaf1, p[4]])

def p_identifiers(p):
	''' identifiers : identifiers COMMA IDENTIFIER 
					| IDENTIFIER'''
	if len(p)==2:
		leaf1 = leaf_gen(Dict["IDENTIFIER"],p[1])
		p[0] = Node(Dict["identifiers"],[leaf1])
	else:
		leaf1 = leaf_gen(Dict["COMMA"],p[2])
		leaf2 = leaf_gen(Dict["IDENTIFIER"],p[3])
		p[0] = Node(Dict["identifiers"],[p[1],leaf1,leaf2])



def p_variable_declaration_body_2(p): # eg. var (x:Int,y:Array[String],z) = (2,new Array[String](5),3);
	'''variable_declaration_body : LPAREN variable_list RPAREN ASOP LPAREN variable_argument_list RPAREN'''	
	leaf1 = leaf_gen(Dict["LPAREN"], p[1])
	leaf2 = leaf_gen(Dict["RPAREN"], p[3])
	leaf3 = leaf_gen(Dict["ASOP"], p[4])
	leaf4 = leaf_gen(Dict["LPAREN"], p[5])
	leaf5 = leaf_gen(Dict["RPAREN"], p[7])
	p[0] = Node(Dict["variable_declaration_body"], [leaf1, p[2], leaf2, leaf3, leaf4, p[6], leaf5])

def p_variable_list(p):					# eg. x,y:Int,z
	''' variable_list : variable_dec 
					  | variable_list COMMA variable_dec'''
	if len(p)==2:
		p[0] = Node(Dict["variable_list"],[p[1]])
	else:
		leaf1 = leaf_gen(Dict["COMMA"],p[2])
		p[0] = Node(Dict["variable_list"],[p[1],leaf1,p[3]])

def p_variable_dec(p):						# eg. x:Int or x
	''' variable_dec : IDENTIFIER type_opt'''
	leaf1 = leaf_gen(Dict["IDENTIFIER"],p[1])
	p[0] = Node(Dict["variable_dec"],[leaf1,p[2]])

# def p_variable_declaration_body_3(p): # eg. var x,y,z = (a:Int) => a*a;  Notice, x,y,z are functions.
# 	''' variable_declaration_body : identifiers ASOP LPAREN fun_params RPAREN FUNTYPE expression'''      

# 	leaf2 = leaf_gen("ASOP", p[2])
# 	leaf3 = leaf_gen("LPAREN", p[3])
# 	leaf4 = leaf_gen("RPAREN", p[5])
# 	leaf5 = leaf_gen("FUNTYPE", p[6])
# 	p[0] = Node("variable_declaration_body", [p[1], leaf2, leaf3, p[4], leaf4, leaf5,p[7]])


def p_expr_opt(p):
	''' expr_opt : ASOP variable_declaration_initializer 
				 | empty '''
	if len(p) > 2:
		leaf1 = leaf_gen(Dict["ASOP"],p[1])
		p[0] = Node(Dict["expr_opt"],[leaf1,p[2]])
	else:
		p[0] = Node(Dict["expr_opt"],[p[1]])


def p_variable_declarator_id(p):
	'''variable_declarator_id : IDENTIFIER COLON type'''
	leaf1 = leaf_gen(Dict["IDENTIFIER"], p[1])
	leaf2 = leaf_gen(Dict["COLON"], p[2])
	p[0] = Node(Dict["variable_declarator_id"], [leaf1, leaf2, p[3]])


#DATA_TYPES AND VARIABLE_TYPES
def p_type(p):
	'''type : primitive_type 
			| reference_type '''
	p[0] = Node(Dict["type"], [p[1]])

def p_primitive_type(p):
	'''primitive_type : TYPE_INT
						| TYPE_DOUBLE
						| TYPE_CHAR
						| TYPE_STRING
						| TYPE_BOOLEAN 
						| TYPE_VOID   '''
	leaf1 = leaf_gen(Dict["TYPE"], p[1])
	p[0] = Node(Dict["primitive_type"], [leaf1]) 


def p_reference_type(p):
	'''reference_type : class_data_type
					  | array_data_type'''
	p[0] = Node(Dict["reference_type"], [p[1]])

def p_class_data_type(p):
	'''class_data_type : name'''
	p[0] = Node(Dict["class_data_type"], [p[1]])

def p_array_data_type(p):
	'''array_data_type : KEYWORD_ARRAY LBRAC type RBRAC'''
	leaf1 = leaf_gen(Dict["ARRAY"], p[1])
	leaf2 = leaf_gen(Dict["LBRAC"], p[2])
	leaf3 = leaf_gen(Dict["RBRAC"], p[4])
	p[0] = Node(Dict["array_data_type"], [leaf1, leaf2, p[3], leaf3])



#VARIABLE_NAMES
def p_name(p):
		'''name : simple_name
				| qualified_name'''
		p[0] = Node(Dict["name"], [p[1]])


def p_simple_name(p):
		'''simple_name : IDENTIFIER'''
		leaf1 = leaf_gen(Dict["IDENTIFIER"], p[1])
		p[0] = Node(Dict["simple_name"], [leaf1])


def p_qualified_name(p):
		'''qualified_name : name INST simple_name'''
		leaf1 = leaf_gen(Dict["DOT"], p[2])
		p[0] = Node(Dict["qualified_name"], [p[1], leaf1, p[3]])



#INITIALIZERS
def p_array_initializer(p):
	''' array_initializer : KEYWORD_NEW KEYWORD_ARRAY LBRAC type RBRAC LPAREN conditional_or_expression RPAREN
												| KEYWORD_ARRAY LPAREN argument_list_opt RPAREN
												| KEYWORD_ARRAY LBRAC type RBRAC LPAREN argument_list_opt RPAREN
												| multidimensional_array_initializer'''
	if len(p) == 9:
		leaf1 = leaf_gen(Dict["NEW"], p[1])
		leaf2 = leaf_gen(Dict["ARRAY"], p[2])
		leaf3 = leaf_gen(Dict["LBRAC"], p[3])
		leaf4 = leaf_gen(Dict["RBRAC"], p[5])
		leaf5 = leaf_gen(Dict["LPAREN"], p[6])
		leaf7 = leaf_gen(Dict["RPAREN"], p[8])

		p[0] = Node(Dict["array_initializer"], [leaf1, leaf2, leaf3, p[4], leaf4, leaf5, p[6], leaf7])
	
	elif len(p)==8:
		leaf2 = leaf_gen(Dict["ARRAY"], p[1])
		leaf3 = leaf_gen(Dict["LBRAC"], p[2])
		leaf4 = leaf_gen(Dict["RBRAC"], p[4])
		leaf5 = leaf_gen(Dict["LPAREN"], p[5])
		leaf7 = leaf_gen(Dict["RPAREN"], p[7])

		p[0] = Node(Dict["array_initializer"], [leaf2, leaf3, p[3], leaf4, p[5],leaf7])		
	
	elif len(p) ==2:
		p[0] = Node(Dict["array_initializer"],[p[1]])

	else:
		leaf1 = leaf_gen(Dict["ARRAY"], p[1])
		leaf2 = leaf_gen(Dict["LPAREN"], p[2])
		leaf3 = leaf_gen(Dict["RPAREN"], p[4]) 
		p[0] = Node(Dict["array_initializer"], [leaf1, leaf2, p[3], leaf3])   

def p_multidimensional_array_initializer(p):
	''' multidimensional_array_initializer : KEYWORD_ARRAY INST KEYWORD_OFDIM LBRAC type RBRAC LPAREN argument_list RPAREN'''
	leaf1 = leaf_gen(Dict["ARRAY"],p[1])
	leaf2 = leaf_gen(Dict["DOT"],p[2])
	leaf3 = leaf_gen(Dict["OFDIM"],p[3])
	leaf4 = leaf_gen(Dict["LBRAC"],p[4])
	leaf5 = leaf_gen(Dict["RBRAC"],p[6])
	leaf6 = leaf_gen(Dict["LPAREN"],p[7])
	leaf7 = leaf_gen(Dict["RPAREN"],p[9])
	p[0] = Node(Dict["multidimensional_array_initializer"],[leaf1,leaf2,leaf3,leaf4,p[5],leaf5,leaf6,p[8],leaf7])

def p_class_initializer(p):
	''' class_initializer : KEYWORD_NEW name LPAREN argument_list_opt RPAREN ''' 
	leaf1 = leaf_gen(Dict["NEW"], p[1])
	leaf2 = leaf_gen(Dict["LPAREN"], p[3])
	leaf3 = leaf_gen(Dict["RPAREN"], p[5])
	p[0] = Node(Dict["class_initializer"], [leaf1, p[2], leaf2, p[4], leaf3])



# STATEMENTS
def p_statement(p):
        '''statement : normal_statement 
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | do_while_statement
                     | for_statement'''
        p[0] = Node(Dict["statement"], [p[1]])

def p_normal_statement(p):
	'''normal_statement : block 
						| expression_statement
						| empty_statement
						| return_statement'''

	p[0] = Node(Dict["normal_statement"], [p[1]])
 
def p_expression_statement(p):
	'''expression_statement : statement_expression TERMINATOR'''
	leaf1 = leaf_gen(Dict["STATE_END"], p[2])
	p[0] = Node(Dict["expression_statement"], [p[1], leaf1])
															 

def p_statement_expression(p):
	'''statement_expression : assignment
							| method_invocation'''
			
	p[0] = Node(Dict["statement_expression"], [p[1]])

#to do dict

#IF THEN STATEMENT
def p_if_then_statement(p):
	'''if_then_statement : KEYWORD_IF LPAREN expression RPAREN statement'''
	leaf1 = leaf_gen(Dict["IF"],p[1])
	leaf2 = leaf_gen(Dict["LPAREN"],p[2])
	leaf3 = leaf_gen(Dict["RPAREN"],p[4])
	p[0] = Node(Dict["if_then_statement"],[leaf1,leaf2,p[3],leaf3,p[5]])

def p_if_then_else_statement(p):
        '''if_then_else_statement : KEYWORD_IF LPAREN expression RPAREN if_then_else_intermediate KEYWORD_ELSE statement'''
        leaf1 = leaf_gen(Dict["IF"], p[1])
        leaf2 = leaf_gen(Dict["LPAREN"], p[2])
        leaf3 = leaf_gen(Dict["RPAREN"], p[4])
        leaf4 = leaf_gen(Dict["ELSE"], p[6])
        p[0] = Node(Dict["if_then_else_statement"], [leaf1, leaf2, p[3], leaf3, p[5], leaf4, p[7]])
       

def p_if_then_else_statement_precedence(p):
        '''if_then_else_statement_precedence : KEYWORD_IF LPAREN expression RPAREN if_then_else_intermediate KEYWORD_ELSE if_then_else_intermediate'''
        leaf1 = leaf_gen(Dict["IF"], p[1])
        leaf2 = leaf_gen(Dict["LPAREN"], p[2])
        leaf3 = leaf_gen(Dict["RPAREN"], p[4])
        leaf4 = leaf_gen(Dict["ELSE"], p[6])
        p[0] = Node(Dict["if_then_else_statement_precedence"], [leaf1, leaf2, p[3], leaf3, p[5], leaf4, p[7]])
      

def p_if_then_else_intermediate(p):
        '''if_then_else_intermediate : normal_statement
                                     | if_then_else_statement_precedence'''
        p[0] = Node(Dict["if_then_else_intermediate"], [p[1]]) 		 

# WHILE_LOOP
def p_while_statement(p):
	'''while_statement : KEYWORD_WHILE LPAREN expression RPAREN statement'''
	leaf1 = leaf_gen(Dict["WHILE"], p[1])
	leaf2 = leaf_gen(Dict["LPAREN"], p[2])
	leaf3 = leaf_gen(Dict["RPAREN"], p[4])
	p[0] = Node(Dict["while_statement"], [leaf1, leaf2, p[3], leaf3, p[5]])
	
#DO_WHILE_LOOP
def p_do_while_statement(p):
	'''do_while_statement : KEYWORD_DO statement KEYWORD_WHILE LPAREN expression RPAREN TERMINATOR '''
	leaf1 = leaf_gen(Dict["DO"], p[1])
	leaf2 = leaf_gen(Dict["WHILE"], p[3])
	leaf3 = leaf_gen(Dict["LPAREN"], p[4])
	leaf4 = leaf_gen(Dict["RPAREN"], p[6])
	leaf5 = leaf_gen(Dict["STATE_END"], p[7])
	p[0] = Node(Dict["do_while_statement"], [leaf1, p[2], leaf2, leaf3, p[5], leaf4, leaf5])
			 
# FOR_LOOP
def p_for_statement1(p):
	'''for_statement : KEYWORD_FOR LPAREN for_logic RPAREN statement'''
	leaf1 = leaf_gen (Dict["FOR"],p[1])
	leaf2 = leaf_gen (Dict["LPAREN"],p[2])
	leaf3 = leaf_gen (Dict["RPAREN"],p[4])
	p[0] = Node(Dict["for_statement"],[leaf1,leaf2,p[3],leaf3,p[5]])

def p_for_statement2(p):
	'''for_statement : KEYWORD_FOR BLOCKBEGIN for_logic BLOCKEND statement'''
	leaf1 = leaf_gen (Dict["FOR"],p[1])
	leaf2 = leaf_gen (Dict["BLOCKBEGIN"],p[2])
	leaf3 = leaf_gen (Dict["BLOCKEND"],p[4])
	p[0] = Node(Dict["for_statement"],[leaf1,leaf2,p[3],leaf3,p[5]])

def p_for_logic(p):
		''' for_logic : for_update 
									| for_update TERMINATOR for_logic '''
		if len(p)==2:
			p[0]=Node(Dict["for_logic"],[p[1]])
		else:
			leaf1 = leaf_gen(Dict["STATE_END"],p[2])
			p[0] = Node(Dict["for_logic"],[p[1],leaf1,p[3]])

def p_for_update(p):
	''' for_update : for_loop for_step_opts '''
	p[0]=Node(Dict["for_update"],[p[1],p[2]])

def p_for_loop(p):
	''' for_loop : IDENTIFIER CHOOSE expression for_untilTo expression '''
	
	leaf1 = leaf_gen(Dict["IDENTIFIER"],p[1])
	leaf2 = leaf_gen(Dict["CHOOSE"],p[2])
	p[0] = Node(Dict["for_loop_st"],[leaf1,leaf2,p[3],p[4],p[5]])

def p_for_untilTo(p):
	'''for_untilTo : KEYWORD_UNTIL 
									| KEYWORD_TO'''

	leaf1 = leaf_gen(Dict["UNTIL_TO"],p[1])
	p[0]=Node(Dict["for_untilTo"],[leaf1])


def p_for_step_opts(p):
	''' for_step_opts : KEYWORD_BY expression
										| empty'''
	if len(p)==2:
		p[0]=Node(Dict["for_step_opts"],[p[1]])
	else :
		leaf1 = leaf_gen(Dict["BY"],p[1])
		p[0]=Node(Dict["for_step_opts"],[leaf1,p[2]])


#to dict
#EMPTY STATEMENT
def p_empty_statement(p):
				'''empty_statement : TERMINATOR '''
				leaf1 = leaf_gen(Dict["STATE_END"], p[1])
				p[0] = Node(Dict["empty_statement"], [leaf1])

#RETURN STATEMENT
def p_return_statement(p):
				'''return_statement : KEYWORD_RETURN expression_optional TERMINATOR '''
				leaf1 = leaf_gen(Dict["RETURN"], p[1])
				leaf2 = leaf_gen(Dict["STATE_END"], p[3])
				p[0] = Node(Dict["return_statement"], [leaf1, p[2], leaf2])



# CLASS DECLARATION
def p_class_declaration(p):
	'''class_declaration : class_header class_body'''
	p[0] = Node(Dict["class_declaration"], [p[1], p[2]])

def p_class_header(p):
	'''class_header : KEYWORD_CLASS simple_name modifier_opts class_param_clause_opt class_template_opt'''
	leaf1 = leaf_gen(Dict["CLASS"],p[1])
	p[0] = Node(Dict["class_header"],[leaf1,p[2],p[3],p[4],p[5]])

def p_class_param_clause_opt(p):
	'''class_param_clause_opt : class_param_clause 
							  | empty'''
	p[0] = Node(Dict["class_param_clause_opt"],[p[1]])

def p_class_param_clause(p):
	'''class_param_clause : LPAREN class_params_opt RPAREN'''
	leaf1 = leaf_gen(Dict["LPAREN"],p[1])
	leaf2 = leaf_gen(Dict["RPAREN"],p[3])
	p[0] = Node(Dict["class_param_clause"],[leaf1,p[2],leaf2])

def p_class_param_opt(p):
	'''class_params_opt : class_params
					 	| empty '''
	p[0] = Node(Dict["class_param_opt"],[p[1]])

def p_class_params(p):
	'''class_params : class_param
					| class_params COMMA class_param'''
	if len(p)==2:
		p[0] = Node(Dict["class_params"],[p[1]])
	else:
		leaf1 = leaf_gen(Dict["COMMA"],p[2])
		p[0] = Node(Dict["class_params"],[p[1],leaf1,p[3]])

def p_class_param(p):
	'''class_param : class_declaration_keyword_opt variable_declarator_id expr_opt'''
	p[0] = Node(Dict["class_param"],[p[1],p[2],p[3]])

def p_override_opt(p):
	'''override_opt : override
					 | empty'''
	p[0] = Node(Dict["override_opt"],[p[1]])

def p_override(p):
	'''override : KEYWORD_OVERRIDE'''
	leaf1 = leaf_gen(Dict["OVERRIDE"],p[1])
	p[0] = Node(Dict["override"],[leaf1])

def p_class_declaration_keyword_opt(p):
	'''class_declaration_keyword_opt : override_opt modifier_opts declaration_keyword 
									 | empty '''
	if len(p)==4:
		p[0] = Node(Dict["class_declaration_keyword_opt"],[p[1],p[2],p[3]])
	else:
		p[0] = Node(Dict["class_declaration_keyword_opt"],[p[1]])

def p_type_opt(p):
	'''type_opt : COLON type 
				| empty'''
	if len(p)==2:
		p[0] = Node(Dict["type_opt"],[p[1]])
	else:
		leaf1 = leaf_gen(Dict["COLON"],p[1])
		p[0] = Node(Dict["type_opt"],[leaf1,p[2]])

def p_class_template_opt(p):
	'''class_template_opt : class_template 
						  | empty '''
	p[0] = Node(Dict["class_template_opt"],[p[1]])


def p_class_template(p):
	'''class_template : KEYWORD_EXTENDS simple_name LPAREN variable_list RPAREN'''
	leaf1 = leaf_gen(Dict["KEYWORD_EXTENDS"], p[1])
	leaf2 = leaf_gen(Dict["LPAREN"], p[3])
	leaf3 = leaf_gen(Dict["RPAREN"], p[5])
	p[0] = Node(Dict["class_header_extends"], [leaf1, p[2], leaf2, p[4], leaf3])

def p_class_body(p):
	'''class_body : block ''' 
	p[0] = Node(Dict["class_body"], [p[1]])


#METHOD DECLARATION
def p_method_declaration1(p):
	'''method_declaration : method_header method_body'''
	p[0] = Node(Dict["method_declaration"], [p[1], p[2]])

# def p_method_declaration2(p):
# 	'''method_declaration : KEYWORD_DEF fun_sig block'''
# 	leaf1 = leaf_gen("DEF",p[1])
# 	p[0] = Node("method_declaration",[leaf1,p[2],p[3]])

def p_method_header(p):
	'''method_header : KEYWORD_DEF fun_def'''
	leaf1 = leaf_gen(Dict["DEF"],p[1])
	p[0] = Node(Dict["method_header"],[leaf1,p[2]])

def p_fun_def1(p):
	'''fun_def : fun_sig type_opt ASOP'''
	leaf1 = leaf_gen(Dict["ASOP"],p[3])
	p[0] = Node(Dict["fun_def"],[p[1],p[2],leaf1])

def p_fun_def2(p):
	'''fun_def : fun_sig type_opt'''
	# leaf1 = leaf_gen("ASOP",p[3])
	p[0] = Node(Dict["fun_def"],[p[1],p[2]])

def p_fun_sig(p):
	'''fun_sig : simple_name fun_param_clause'''
	p[0] = Node(Dict["fun_sig"],[p[1],p[2]])

# def p_fun_param_clause_opt(p):
# 	'''fun_param_clause_opt : fun_param_clause
# 							| empty'''
# 	p[0] = Node("fun_param_clause_opt",[p[1]])

def p_fun_param_clause(p):
	'''fun_param_clause : LPAREN fun_params_opt RPAREN  '''
	leaf1 = leaf_gen(Dict["LPAREN"],p[1])
	leaf2 = leaf_gen(Dict["RPAREN"],p[3])
	p[0] = Node(Dict["fun_param_clause"],[leaf1,p[2],leaf2])

def p_fun_params_opt(p):
	'''fun_params_opt : fun_params
					| empty'''
	p[0] = Node(Dict["fun_params_opt"],[p[1]])

def p_fun_params(p):
	'''fun_params : fun_param 
				  | fun_params COMMA fun_param'''
	if len(p)==2:
		p[0] = Node(Dict["fun_params"],[p[1]])
	else:
		leaf1 = leaf_gen(Dict["COMMA"],p[2])
		p[0] = Node(Dict["fun_params"],[p[1],leaf1,p[3]])

def p_fun_param(p):
	'''fun_param : variable_declarator_id expr_opt'''
	p[0] = Node(Dict["fun_param"],[p[1],p[2]])

def p_method_body(p):
	'''method_body : block 
					| variable_declaration_initializer''' 
	p[0] = Node(Dict["method_body"], [p[1]])


#EMPTY RULE
def p_empty(p):
		'empty :'
		leaf1 = leaf_gen("", "")
		p[0] = Node(Dict["empty"], [leaf1])
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



