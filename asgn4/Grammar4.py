class Node(object): 
   count = 1

   def __init__(self,name,children):
      self.name = name #name of the node, non terminal
      self.children = children
      self.id=Node.count
      Node.count+=1


def create_children(token_name , terminal_name):
   leaf_t = Node(terminal_name,[])
   leaf_token = Node(token_name,[leaf_t])
   return leaf_token

'''PROGRAM '''

def p_compilation_unit(p):
   '''compilation_unit : class_and_obj_declarations'''

   p[0]  = Node("compilationUnit", [p[1]])

'''DECLARATIONS'''

def p_class_and_obj_declarations(p):
   '''class_and_obj_declarations : class_and_obj_declaration 
      | class_and_obj_declarations class_and_obj_declaration'''

   if(len(p) == 2):
      p[0] = Node("class_and_obj_declarations", [p[1]])

   else:
      p[0] = Node("class_and_obj_declarations", [p[1], p[2]])

def p_class_and_obj_declaration(p):
   '''class_and_obj_declaration : singleton_object 
      | class_declaration '''

   p[0]  = Node("class_and_obj_declaration", [p[1]])

def p_singleton_object(p):
   '''singleton_object : object_declaration block'''

   p[0]  = Node("singleton_object", [p[1], p[2]])

def p_object_declaration(p):
   '''object_declaration : KW_OBJ name'''

   leaf1 = create_children("KW_OBJ", p[1])
   p[0]  = Node("object_declaration", [leaf1, p[2]])
#
#def p_class_declaration(p):
#   '''class_declaration : KW_class name class_body'''
#
#   leaf1 = create_children("KW_class", p[1])
#   p[0]  = Node("class_declaration", [leaf1, p[2], p[3]])

'''BLOCK DEFINITION'''

def p_block(p):
   '''block : LCURLY block_stats_star RCURLY'''

   leaf1 = create_children("LCURLY", p[1])
   leaf3 = create_children("RCURLY", p[3])
   p[0]  = Node("block", [leaf1, p[2], leaf3])

def p_block_stats_star(p):
   '''block_stats_star : block_stats | empty '''

   p[0]  = Node("block_stats_star", [p[1]])   

def p_block_stats(p):
   '''block_stats : block_stat | block_stats block_stat'''

   if(len(p) == 2):
      p[0] = Node("block_stats", [p[1]])

   else:
      p[0] = Node("block_stats", [p[1], p[2]])

def p_block_stat(p):
   '''block_stat : local_variable_declaration_statement 
				| statement 
				| class_and_obj_declaration 
				| method_declaration'''

   p[0] = Node("block_stat", [p[1]])

'''EXPRESSION'''

def p_expression_question(p):
   '''expression_question : expression | empty '''


   p[0] = Node("expression_question", [p[1]])

def p_expression(p):
   '''expression : assignment_expression '''


   p[0] = Node("expression", [p[1]])

def p_assignment_expression(p):
   '''assignment_expression : assignment 
			   | conditional_or_expression
			   | if_else_expression '''


   p[0] = Node("assignment_expression", [p[1]])

def p_if_else_expression(p):
   ''' if_else_expression : KW_if LPAREN expression RPAREN expression KW_else expression '''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("LPAREN", p[2])
   leaf4 = create_children("RPAREN", p[4])
   leaf6 = create_children("KW_else", p[6])
   p[0] = Node("if_else_expression", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]])


def p_assignment(p):
   ''' assignment : left_hand_side assignment_operator assignment_expression '''

   p[0] = Node("assignment", [p[1],p[2],p[3]])

def p_left_hand_side(p):
   ''' left_hand_side : id | array_access '''


   p[0] = Node("left_hand_side", [p[1]])

def p_id(p):
   ''' id : name | qualified_id '''

   p[0] = Node("id", [p[1]])

def p_qualified_id(p):
   '''qualified_id : name KW_DOT name '''

   p[0] = Node("qualified_id", [p[1],p[2],p[3]])

def p_name(p):
   '''name : IDENTIFIER '''

   leaf1 = create_children("IDENTIFIER", p[1])
   p[0] = Node("name", [leaf1])


def p_array_access(p):
   ''' array_access : id dimension '''

   p[0]  = Node("array_access", [p[1], p[2]])

def p_dimension(p):
   ''' dimension : dimension KW_LSQB expression KW_RSQB | KW_LSQB expression KW_RSQB '''

   if(len(p) == 4):		
      leaf1 = create_children("KW_LSQB", p[1])
      leaf3 = create_children("KW_RSQB", p[3])
      p[0] = Node("class_and_obj_declarations", [leaf1,p[2],leaf3])

   else:
      leaf2 = create_children("KW_LSQB", p[2])
   	  leaf4 = create_children("KW_RSQB", p[4])
      p[0] = Node("class_and_obj_declarations", [p[1], leaf2, p[3], leaf4])


def p_assignment_operator(p):
   ''' assignment_operator : = | *= | /= | %= | += | -= | <<= | >>= | >>>= | &= | ^= | |= '''

   leaf1 = create_children("LF_AssignOp", p[1])
   p[0] = Node("assignment_operator", [leaf1])

 def p_conditional_or_expression(p):
   ''' conditional_or_expression : conditional_and_expression | conditional_or_expression KW_OR conditional_and_expression '''

   if(len(p) == 2):
      p[0] = Node("conditional_or_expression", [p[1]])

   else:
      leaf2 = create_children("KW_OR", p[2])
      p[0] = Node("conditional_or_expression", [p[1], leaf2, p[3]])

 def p_inclusive_or_expression(p):
   '''inclusive_or_expression : exclusive_or_expression  | inclusive_or_expression KW_OR_BITWISE exclusive_or_expression'''

   if(len(p) == 2):
      p[0] = Node("inclusive_or_expression", [p[1]])

   else:
      leaf2 = create_children("KW_OR_BITWISE", p[2])
      p[0] = Node("inclusive_or_expression", [p[1], leaf2, p[3]])

 def p_exclusive_or_expression(p):
   ''' exclusive_or_expression : and_expression | exclusive_or_expression KW_XOR and_expression '''

   if(len(p) == 2):
      p[0] = Node("exclusive_or_expression", [p[1]])

   else:
      leaf2 = create_children("KW_XOR", p[2])
      p[0] = Node("exclusive_or_expression", [p[1], leaf2, p[3]])

 def p_and_expression(p):
   ''' and_expression : equality_expression | and_expression KW_AND_BITWISE equality_expression '''

   if(len(p) == 2):
      p[0] = Node("and_expression", [p[1]])

   else:
      leaf2 = create_children("KW_AND_BITWISE", p[2])
      p[0] = Node("and_expression", [p[1], leaf2, p[3]])


def p_equality_expression(p):
   '''equality_expression : relational_expression
								| equality_expression KW_EQUAL relational_expression
								| equality_expression KW_NEQUAL relational_expression'''


   if(len(p) == 2):
      p[0] = Node("equality_expression", [p[1]])

   else:
      leaf2 = create_children("LF_equalityOp", p[2])
      p[0] = Node("equality_expression", [p[1], leaf2, p[3]])

def p_relational_expression(p):
   '''relational_expression : shift_expression
								 | relational_expression KW_GREATER shift_expression
								 | relational_expression KW_LESS shift_expression
								 | relational_expression KW_GEQ shift_expression
								 | relational_expression KW_LEQ shift_expression'''

   if(len(p) == 2):
      p[0] = Node("equality_expression", [p[1]])

   else:
      leaf2 = create_children("LF_relationalOp", p[2])
      p[0] = Node("equality_expression", [p[1], leaf2, p[3]])


def p_shift_expression(p):
   '''shift_expression : additive_expression
									| shift_expression KW_LSHIFT additive_expression
									| shift_expression KW_RSHIFT additive_expression'''

   if(len(p) == 2):
      p[0] = Node("shift_expression", [p[1]])

   else:
      leaf2 = create_children("LF_shiftOp", p[2])
      p[0] = Node("shift_expression", [p[1], leaf2, p[3]])



def p_additive_expression(p):
   '''additive_expression : multiplicative_expression
								 | additive_expression KW_PLUS multiplicative_expression
								 | additive_expression KW_MINUS multiplicative_expression'''

   if(len(p) == 2):
      p[0] = Node("additive_expression", [p[1]])

   else:
      leaf2 = create_children("LF_additiveOp", p[2])
      p[0] = Node("additive_expression", [p[1], leaf2, p[3]])

def p_multiplicative_expression(p):
   '''multiplicative_expression : unary_expression

									 | multiplicative_expression KW_TIMES unary_expression
									 | multiplicative_expression KW_DIVIDE unary_expression
									 | multiplicative_expression KW_REMAINDER unary_expression'''

   if(len(p) == 2):
      p[0] = Node("multiplicative_expression", [p[1]])

   else:
      leaf2 = create_children("LF_multiplicativeOp", p[2])
      p[0] = Node("multiplicative_expression", [p[1], leaf2, p[3]])

def p_unary_expression(p):
   '''unary_expression : PLUS unary_expression
							| KW_MINUS unary_expression
							| unary_expression_not_plus_minus'''

   if(len(p) == 2):
      p[0] = Node("unary_expression", [p[1]])

   else:
      leaf1 = create_children("LF_unaryop", p[1])
      p[0] = Node("unary_expression", [leaf1, p[2]])


def p_unary_expression_not_plus_minus(p):
   '''unary_expression_not_plus_minus : base_variable_set
											 | KW_TILDA unary_expression
											 | KW_NOT unary_expression
											 | cast_expression''' 

   if(len(p) == 2):
      p[0] = Node("unary_expression_not_plus_minus", [p[1]])

   else:
      leaf1 = create_children("LF_unarydiffop", p[1])
      p[0] = Node("unary_expression_not_plus_minus", [leaf1, p[2]])


def p_base_variable_set(p):
   '''base_variable_set : variable_literal
						 | KW_LPAREN expression KW_RPAREN'''

   if(len(p) == 2):
      p[0] = Node("base_variable_set", [p[1]])

   else:
      leaf1 = create_children("KW_LPAREN", p[1])
      leaf3 = create_children("KW_RPAREN", p[3])
      p[0] = Node("base_variable_set", [leaf1, p[2], leaf3])


def p_variable_literal(p):
   '''variable_literal : valid_variable | primary'''

   p[0] = Node("variable_literal", [p[1]])


def p_cast_expression(p):
   '''cast_expression : LPAREN primitive_type RPAREN unary_expression'''

   leaf1 = create_children("LPAREN", p[1])
   leaf3 = create_children("RPAREN", p[3])
   p[0] = Node("cast_expression", [leaf1, p[2], leaf3, p[4]])


def p_primary(p):
   '''primary : literal | method_invocation'''

   p[0] = Node("primary", [p[1]])


def p_literal(p):
   '''literal : int_float	| c_literal ''' 

   p[0] = Node("literal", [p[1]])


def p_c_literal(p):
   '''c_literal : KW_CHAR
					| KW_STRING
					| KW_true
					| KW_false
					| KW_null '''

   leaf1 = create_children("LF_charliteral", p[1])
   p[0] = Node("c_literal", [leaf1])

def p_int_float(p):
   '''int_float : KW_DOUBLE | KW_INT '''

   leaf1 = create_children("LF_intliteral", p[1])
   p[0] = Node("int_float", [leaf1])

#FUNCTION CALLS

def p_method_invocation(p):
   '''method_invocation : id LPAREN argument_list RPAREN '''

   leaf2 = create_children("LPAREN", p[2])
   leaf4 = create_children("RPAREN", p[4])
   p[0] = Node("method_invocation", [p[1], leaf2, p[3], leaf4])


#Check this: argument_list_question is missing

def p_argument_list(p):
   '''argument_list : expression
                  | argument_list KW_comma expression'''

   if(len(p) == 2):
      p[0] = Node("argument_list", [p[1]])

   else:
      leaf2 = create_children("KW_comma", p[2])
      p[0] = Node("argument_list", [p[1], leaf2, p[3]])

'''LOCAL VARIABLE DECLARATION'''

def p_modifier(p):
   ''' modifier : KW_protected | KW_private '''

   leaf1 = create_children("LF_modifier", p[1])
   p[0] = Node("modifier", [leaf1])

def p_modifier_question(p):
   ''' modifier_question : modifier | empty '''

   p[0] = Node("modifier_question", [p[1]])


def p_declaration_keyword(p):
   '''declaration_keyword : KW_var | KW_val '''

   leaf1 = create_children("LF_declaration", p[1])
   p[0] = Node("declaration_keyword", [leaf1])


def p_local_variable_declaration_statement(p):
   '''local_variable_declaration_statement : local_variable_declaration terminator '''

   p[0] = Node("local_variable_declaration_statement", [p[1],p[2]])


def p_terminator(p):
   '''terminator : KW_semi | KW_nl '''

   leaf1 = create_children("LF_terminator", p[1])
   p[0] = Node("terminator", [leaf1])


def p_local_variable_declaration(p):
   '''local_variable_declaration : modifier_question declaration_keyword variable_declaration_body'''

   p[0] = Node("local_variable_declaration", [p[1],p[2],p[3]])


def p_variable_declaration_initializer(p):
   '''variable_declaration_initializer : expression
                              | array_initializer
                                     | class_initializer'''

   p[0] = Node("variable_declaration_initializer", [p[1]])


def p_variable_argument_list(p):
   ''' variable_argument_list : variable_declaration_initializer
                              | variable_argument_list KW_comma variable_declaration_initializer'''

   if(len(p) == 2):
      p[0] = Node("variable_argument_list", [p[1]])

   else:
      leaf2 = create_children("KW_comma", p[2])
      p[0] = Node("variable_argument_list", [p[1], leaf2, p[3]])



def p_variable_argument_body(p):
   '''variable_declaration_body : identifiers type_opt KW_assignment  variable_declaration_initializer 
      | KW_LPAREN variable_list KW_RPAREN KW_assignment KW_LPAREN variable_argument_list KW_RPAREN'''

   if(len(p) == 5):
      leaf3 = create_children("KW_assignment", p[3])
      p[0] = Node("variable_argument_list", [p[1], p[2], leaf3, p[4]])

   else:
      leaf1 = create_children("KW_LPAREN", p[1])
      leaf3 = create_children("KW_RPAREN", p[3])
      leaf4 = create_children("KW_assignment", p[4])
      leaf5 = create_children("KW_LPAREN", p[5])
      leaf7 = create_children("KW_RPAREN", p[7])
      p[0] = Node("variable_argument_list", [leaf1, p[2], leaf3, leaf4, leaf5, p[6], leaf7])


def p_identifiers(p):
   ''' identifiers : identifiers KW_comma KW_IDENTIFIER | KW_IDENTIFIER'''

   if(len(p) == 2):
      leaf1 = create_children("KW_IDENTIFIER", p[1])
      p[0] = Node("identifiers", [leaf1])

   else:
      leaf2 = create_children("KW_comma", p[2])
      leaf3 = create_children("KW_IDENTIFIER", p[3])
      p[0] = Node("identifiers", [p[1], leaf2, leaf3])


def p_variable_list(p):
   ''' variable_list : variable_dec | variable_list KW_comma variable_dec'''

   if(len(p) == 2):
      p[0] = Node("variable_list", [p[1]])

   else:
      leaf2 = create_children("KW_comma", p[2])
      p[0] = Node("variable_list", [p[1], leaf2, p[3]])


def p_variable_dec(p):
   ''' variable_dec : KW_IDENTIFIER type_question'''

   leaf1 = create_children("KW_IDENTIFIER", p[1])
   p[0] = Node("variable_dec", [leaf1, p[2]])


def p_expr_question(p):
   ''' expr_question : KW_assignment variable_declaration_initializer 
             | empty '''

   if(len(p) == 2):
      p[0] = Node("expr_question", [p[1]])

   else:
      leaf1 = create_children("KW_assignment", p[1])
      p[0] = Node("expr_question", [leaf1, p[2]])


def p_variable_declarator_id(p):
   '''variable_declarator_id : KW_IDENTIFIER KW_COLON type'''

   leaf1 = create_children("KW_IDENTIFIER", p[1])
   leaf2 = create_children("KW_COLON", p[2])
   p[0] = Node("variable_declarator_id", [leaf1, leaf2, p[3]])


#DATA_TYPES AND VARIABLE_TYPES

#theirs - ours
#Simple Name - name
#Name - id
#qualified name: qualified_id

def p_type(p):
   '''type : primitive_type | reference_type '''

   p[0] = Node("type", [p[1]])


def p_primitive_type(p):
   '''primitive_type : KW_INT
                  | KW_DOUBLE
                  | KW_CHAR
                  | KW_STRING
                  | KW_BOOLEAN 
                  | KW_VOID   '''


   leaf1 = create_children("LF_primitivetype", p[1])
   p[0] = Node("primitive_type", [leaf1])


def p_reference_type(p):
   '''reference_type : class_data_type | array_data_type'''

   p[0] = Node("reference_type", [p[1]])


def p_class_data_type(p):
   '''class_data_type : id'''

   p[0] = Node("class_data_type", [p[1]])


def p_array_data_type(p):
   '''array_data_type : KW_array KW_LSQB type KW_RSQB'''

   leaf1 = create_children("KW_array", p[1])
   leaf2 = create_children("KW_LSQB", p[2])
   leaf4 = create_children("KW_RSQB", p[4])
   p[0] = Node("array_data_type", [leaf1, leaf2, p[3], leaf4])


# INITIALIZERS

def p_array_initializer(p):
   ''' array_initializer : KW_new KW_array KW_LSQB type KW_RSQB KW_LPAREN conditional_or_expression KW_RPAREN
                                    | KW_array KW_LPAREN argument_list_opt KW_RPAREN
                                    | KW_array KW_LSQB type KW_RSQB KW_LPAREN argument_list_opt KW_RPAREN
                                    | multidimensional_array_initializer'''
   if(len(p) == 2):
      p[0] = Node("array_initializer", [p[1]])

   else if(len(p) == 5):
      leaf1 = create_children("KW_array", p[1])
      leaf2 = create_children("KW_LPAREN", p[2])
      leaf4 = create_children("KW_RPAREN", p[4])
      p[0] = Node("array_initializer", [leaf1, leaf2, p[3], leaf4])
   
   else if(len(p) == 8):
      leaf1 = create_children("KW_array", p[1])
      leaf2 = create_children("KW_LSQB", p[2])
      leaf4 = create_children("KW_RSQB", p[4])
      leaf5 = create_children("KW_LPAREN", p[5])
      leaf7 = create_children("KW_RPAREN", p[7])
      p[0] = Node("array_initializer", [leaf1, leaf2, p[3], leaf4, leaf5, p[6], leaf7])
   else:
      leaf1 = create_children("KW_new", p[1])
      leaf2 = create_children("KW_array", p[2])
      leaf3 = create_children("KW_LSQB", p[3])
      leaf5 = create_children("KW_RSQB", p[5])
      leaf6 = create_children("KW_LPAREN", p[6])
      leaf8 = create_children("KW_RPAREN", p[8])
      p[0] = Node("array_initializer", [leaf1, leaf2, leaf3, p[4], leaf5, leaf6, p[7], leaf8])


def p_multidimensional_array_initializer(p):
   ''' multidimensional_array_initializer : KW_array KW_DOT KW_ofdim KW_LSQB type KW_RSQB KW_LPAREN argument_list KW_RPAREN'''

   leaf1 = create_children("KW_array", p[1])
   leaf2 = create_children("KW_DOT", p[2])
   leaf3 = create_children("KW_ofdim", p[3])
   leaf4 = create_children("KW_LSQB", p[4])
   leaf6 = create_children("KW_RSQB", p[6])
   leaf7 = create_children("KW_LPAREN", p[7])
   leaf9 = create_children("KW_RPAREN", p[9])
   p[0] = Node("multidimensional_array_initializer", [leaf1, leaf2, leaf3, leaf4, p[5], leaf6, leaf7, p[8], leaf9])


def p_class_initializer(p):
   ''' class_initializer : KW_new name KW_LPAREN argument_list_opt KW_RPAREN '''

   leaf1 = create_children("KW_new", p[1])
   leaf3 = create_children("KW_LPAREN", p[3])
   leaf5 = create_children("KW_RPAREN", p[5])
   p[0] = Node("class_initializer", [leaf1, p[2], leaf3, p[4], leaf5])



#Statements
def p_statement(p):
   '''statement : normal_statement 
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement'''

   p[0] = Node("statement", [p[1]])


def p_normal_statement(p):
   '''normal_statement : block 
                  | expression_statement
                  | empty_statement
                  | return_statement'''

   p[0] = Node("normal_statement", [p[1]])


def p_expression_statement(p):
   '''expression_statement : statement_expression terminator'''

   p[0] = Node("expression_statement", [p[1],p[2]])


def p_statement_expression(p):
   '''statement_expression : assignment | method_invocation'''

   p[0] = Node("statement_expression", [p[1]])


#IF THEN STATEMENT
def p_if_then_statement(p):
   '''if_then_statement : KW_if KW_LPAREN expression KW_RPAREN statement'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("KW_LPAREN", p[2])
   leaf4 = create_children("KW_RPAREN", p[4])
   p[0] = Node("if_then_statement", [leaf1, leaf2, p[3], leaf4, p[5]])


def p_if_then_else_statement(p):
   '''if_then_else_statement : KW_if KW_LPAREN expression KW_RPAREN if_then_else_intermediate KW_else statement'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("KW_LPAREN", p[2])
   leaf4 = create_children("KW_RPAREN", p[4])
   leaf6 = create_children("KW_else", p[6])
   p[0] = Node("if_then_else_statement", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]])


def p_if_then_else_statement_precedence(p):
   '''if_then_else_statement_precedence : KW_if KW_LPAREN expression KW_RPAREN if_then_else_intermediate KW_else if_then_else_intermediate'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("KW_LPAREN", p[2])
   leaf4 = create_children("KW_RPAREN", p[4])
   leaf6 = create_children("KW_else", p[6])
   p[0] = Node("if_then_else_statement_precedence", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]])


def p_if_then_else_intermediate(p):
   '''if_then_else_intermediate : normal_statement
                                     | if_then_else_statement_precedence'''

   p[0] = Node("if_then_else_intermediate", [p[1]])


def p_while_statement(p):
   '''while_statement : KW_while KW_LPAREN expression KW_RPAREN statement'''

   leaf1 = create_children("KW_while", p[1])
   leaf2 = create_children("KW_LPAREN", p[2])   
   leaf4 = create_children("KW_RPAREN", p[4])
   p[0] = Node("while_statement", [leaf1, leaf2, p[3], leaf4, p[5]])

# FOR_LOOP

def p_for_statement(p):
   '''for_statement : KW_for KW_LPAREN for_logic KW_RPAREN statement | KEYWORD_FOR KW_LCURL for_logic KW_RCURL statement'''

   leaf1 = create_children("KW_for", p[1])
   leaf2 = create_children("KW_LPAREN", p[2])
   leaf4 = create_children("KW_RPAREN", p[4])
   p[0] = Node("for_statement", [leaf1, leaf2, p[3], leaf4, p[5]])


def p_for_logic(p):
   ''' for_logic : for_update | for_update terminator for_logic '''

   if(len(p) == 2):
      p[0] = Node("for_logic", [p[1]])

   else:
      p[0] = Node("for_logic", [p[1], p[2], p[3]])


def p_for_update(p):
   ''' for_update : for_loop for_step_opts '''

   p[0] = Node("for_update", [p[1], p[2],p[3]])


def p_for_loop(p):
   ''' for_loop : KW_IDENTIFIER KW_choose expression for_untilTo expression '''

   leaf1 = create_children("KW_IDENTIFIER", p[1])
   leaf2 = create_children("KW_choose", p[2])
   p[0] = Node("for_loop", [leaf1, leaf2, p[3], p[4], p[5]])


def p_for_untilTo(p):
   '''for_untilTo : KW_until | KW_to'''

   leaf1 = create_children("LF_untito", p[1])
   p[0] = Node("for_untilTo", [p[1]])


def p_for_step_opts(p):
   ''' for_step_opts : KW_by expression | empty'''

   if len(p)==2:
      p[0]=Node("for_step_opts",[p[1]])

   else :
      leaf1 = create_children("KW_by", p[1])
      p[0]=Node("for_step_opts",[leaf1, p[2]])


def p_empty_statement(p):
   '''empty_statement : terminator '''

   p[0] = Node("empty_statement", [p[1]])


def p_return_statement(p):
   '''return_statement : KW_return expression_optional terminator '''

   leaf1 = create_children("KW_return", p[1])
   p[0] = Node("return_statement", [leaf1, p[2], p[3]])


# CLASS DECLARATION

def p_class_declaration(p):
   '''class_declaration : class_header class_body'''

   p[0] = Node("class_declaration", [p[1],p[2]])


def p_class_header(p):
   '''class_header : KW_CLASS name modifier_opts class_param_clause_question class_template_question'''

   leaf1 = create_children("KW_CLASS", p[1])
   p[0] = Node("class_header", [leaf1, p[2], p[3], p[4], p[5]])


def p_class_param_clause_question(p):
   '''class_param_clause_question : class_param_clause 
                       | empty'''

   p[0] = Node("class_param_clause_question", [p[1]])


def p_class_param_clause(p):
   '''class_param_clause : KW_LPAREN class_params_question KW_RPAREN'''

   leaf1 = create_children("KW_LPAREN", p[1])
   leaf3 = create_children("KW_RPAREN", p[3])
   p[0] = Node("class_param_clause", [leaf1, p[2], leaf3])


def p_class_params_question(p):
   '''class_params_question : class_params
                  | empty '''

   p[0] = Node("class_params_opt", [p[1]])


def p_class_params(p):
   '''class_params : class_param
               | class_params KW_comma class_param'''

   if(len(p) == 2):
      p[0] = Node("class_params", [p[1]])

   else:
      leaf2 = create_children("KW_comma", p[2])
      p[0] = Node("class_params", [p[1], leaf2, p[3]])


def p_class_param(p):
   '''class_param : class_declaration_keyword_question variable_declarator_id expr_question'''

   p[0] = Node("class_param", [p[1],p[2],p[3]])


def p_override_question(p):
   '''override_question : override
                | empty'''

   p[0] = Node("override_question", [p[1]])


def p_override(p):
   '''override : KW_override'''

   leaf1 = create_children("KW_override", p[1])
   p[0] = Node("override", [leaf1])


def p_class_declaration_keyword_question(p):
   '''class_declaration_keyword_question : override_question modifier_question declaration_keyword 
                            | empty '''

   if(len(p) == 2):
      p[0] = Node("class_declaration_keyword_question", [p[1]])

   else:
      p[0] = Node("class_declaration_keyword_question", [p[1], p[2],p[3]])


def p_type_question(p):
   '''type_question : KW_colon type 
            | empty'''

   if len(p)==2:
      p[0] = Node("type_question",[p[1]])

   else:
      leaf1 = create_children("KW_colon",p[1])
      p[0] = Node("type_question",[leaf1, p[2]])


def p_class_template_question(p):
   '''class_template_question : class_template 
                    | empty '''

   p[0] = Node("class_template_question", [p[1]])


def p_class_template(p):
   '''class_template : KW_extends name KW_LPAREN variable_list KW_RPAREN'''

   leaf1 = create_children("KW_extends", p[1])
   leaf3 = create_children("KW_LPAREN", p[3])
   leaf5 = create_children("KW_RPAREN", p[5])
   p[0] = Node("class_template", [leaf1, p[2], leaf3, p[4], leaf5])


def p_class_body(p):
   '''class_body : block ''' 

   p[0] = Node("class_body", [p[1]])


# Method Declaration

def p_method_declaration(p):
   '''method_declaration : method_header method_body'''

   p[0] = Node("method_declaration", [p[1],p[2]])


def p_method_header(p):
   '''method_header : KW_def fun_def'''

   leaf1 = create_children("KW_def", p[1])
   p[0] = Node("method_header", [leaf1,p[2]])


def p_fun_def(p):
   '''fun_def : fun_sig type_opt KW_assignment 
                            | fun_sig type_opt'''

   if(len(p) == 3):
      p[0] = Node("fun_def", [p[1], p[2]])

   else:
      leaf3 = create_children("KW_assignment", p[3])      
      p[0] = Node("fun_def", [p[1], p[2], leaf3])


def p_fun_sig(p):
   '''fun_sig : name fun_param_clause'''

   p[0] = Node("fun_sig", [p[1]])


def p_fun_param_clause(p):
   '''fun_param_clause : KW_LPAREN fun_params_question KW_RPAREN  '''

   leaf1 = create_children("KW_LPAREN", p[1])
   leaf3 = create_children("KW_RPAREN", p[3])
   p[0] = Node("fun_param_clause", [leaf1, p[2], leaf3])


def p_fun_params_question(p):
   '''fun_params_question : fun_params | empty'''

   p[0] = Node("fun_params_question", [p[1]])


def p_fun_params(p):
   '''fun_params : fun_param | fun_params KW_comma fun_param'''

   if(len(p) == 2):
      p[0] = Node("fun_params", [p[1]])

   else:
      leaf2 = create_children("KW_comma", p[2])
      p[0] = Node("fun_params", [p[1], leaf2, p[3]])


def p_fun_param(p):
   '''fun_param : variable_declarator_id expr_opt'''

   p[0] = Node("fun_param", [p[1],p[2]])


def p_method_body(p):
   '''method_body : block | variable_declaration_initializer''' 

   p[0] = Node("method_body", [p[1]])

#EMPTY DEFINITION

def p_empty(p):
   '''empty:'''
   leaf1 = create_children("", "")
   p[0] = Node("empty", [leaf1])
   pass



LEAF_NODES = [ 'IDENTIFIER',
    'NEWLINE_NL',
    'TOK_SEMI',
    'INTEGER_LITS',
    'F_POINT_LITS',
    'BOOLEAN_LITS',
    'CHAR_LITS',
    'STR_LITS',
    'WSPACE_LIT',
    'TOK_LPAREN',
    'TOK_RPAREN',
    'TOK_LSQB',
    'TOK_RSQB',
    'TOK_LCUR',
    'TOK_RCUR',
    'SQUOTES',
    'DQUOTES',
    'COMMENT_LINE',
    'COMMENT_BLOCK',
    'TOK_MINUS',
   'TOK_COLON',
   'TOK_EQ',
   'TOK_EQ_GT',
   'TOK_LT_MINUS',
   'TOK_LE_COLON',
   'TOK_LT_PERCENT',
   'TOK_GT_COLON',
   'TOK_HASH',
   'TOK_AT',
   'TOK_COMMA',
   'TOK_abstract',
   'TOK_case',
   'TOK_catch',
   'TOK_class',
   'TOK_def',
   'TOK_do',
   'TOK_else',
   'TOK_extends',
   'TOK_false',
   'TOK_final',
   'TOK_finally',
   'TOK_for',
   'TOK_forSome',
   'TOK_if',
   'TOK_implicit',
   'TOK_import',
   'TOK_lazy',
   'TOK_match',
   'TOK_new',
   'TOK_null',
   'TOK_object',
   'TOK_override',
   'TOK_package',
   'TOK_private',
   'TOK_protected',
   'TOK_return',
   'TOK_sealed',
   'TOK_super',
   'TOK_this',
   'TOK_throw',   
   'TOK_trait',
   'TOK_Try',
   'TOK_true',
   'TOK_type',
   'TOK_until',
   'TOK_TO',
   'TOK_OFDIM',
   'TOK_val',
   'TOK_var',
   'TOK_while',
   'TOK_with',
   'TOK_yield',
   'TOK_PLUS',
   'TOK_STAR',
   'TOK_DOT',
   'TOK_UNDERSCORE',
   'TOK_ASSIGN',
   'TOK_AT',
   'TOK_EXCLAIM',
   'TOK_COMMA',
   'TOK_HASH',
   'TOK_SEMI',
         ]
