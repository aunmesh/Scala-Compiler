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
   '''object_declaration : KW_OBJ IDENTIFIER'''

   p[0]  = Node("object_declaration", [p[1], p[2]])

def p_class_declaration(p):
   '''class_declaration : KW_class IDENTIFIER class_body'''

   leaf1 = create_children("KW_class", p[1])
   p[0]  = Node("class_declaration", [leaf1, p[2], p[3]])

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


   p[0] = Node("if_else_expression", [p[1],p[2],p[3],p[4],p[5],p[6],p[7]])


def p_assignment(p):
   ''' assignment : left_hand_side assignment_operator assignment_expression '''

   p[0] = Node("assignment", [p[1],p[2],p[3]])

def p_left_hand_side(p):
   ''' left_hand_side : id | array_access '''


   p[0] = Node("left_hand_side", [p[1]])

def p_id(p):
   ''' id : IDENTIFIER | qualified_id '''


   p[0] = Node("id", [p[1]])

def p_qualified_id(p):
   ''' qualified_id : IDENTIFIER KW_DOT IDENTIFIER '''

   p[0] = Node("qualified_id", [p[1],p[2],p[3]])

def p_name(p):
   ''' name : IDENTIFIER '''


   p[0] = Node("name", [p[1]])


def p_array_access(p):
   ''' array_access : id dimension '''

   p[0]  = Node("array_access", [p[1], p[2]])

def p_dimension(p):
   ''' dimension : dimension KW_LSQB expression KW_RSQB | KW_LSQB expression KW_RSQB '''


   if(len(p) == 4):
      p[0] = Node("dimension", [p[1],p[2],p[3]])

   else:
      p[0] = Node("dimension", [p[1], p[2],p[3],p[4]])

def p_assignment_operator(p):
   ''' assignment_operator : = | *= | /= | %= | += | -= | <<= | >>= | >>>= | &= | ^= | |= '''


   p[0] = Node("assignment_operator", [p[1]])

 def p_conditional_or_expression(p):
   ''' conditional_or_expression : conditional_and_expression | conditional_or_expression KW_OR conditional_and_expression '''



   if(len(p) == 2):
      p[0] = Node("conditional_or_expression", [p[1]])

   else:
      p[0] = Node("conditional_or_expression", [p[1], p[2],p[3]])

 def p_inclusive_or_expression(p):
   '''inclusive_or_expression : exclusive_or_expression  | inclusive_or_expression KW_OR_BITWISE exclusive_or_expression'''



   if(len(p) == 2):
      p[0] = Node("inclusive_or_expression", [p[1]])

   else:
      p[0] = Node("inclusive_or_expression", [p[1], p[2],p[3]])

 def p_exclusive_or_expression(p):
   ''' exclusive_or_expression : and_expression | exclusive_or_expression KW_XOR and_expression '''



   if(len(p) == 2):
      p[0] = Node("exclusive_or_expression", [p[1]])

   else:
      p[0] = Node("exclusive_or_expression", [p[1], p[2],p[3]])

 def p_and_expression(p):
   ''' and_expression : equality_expression | and_expression KW_AND_BITWISE equality_expression '''



   if(len(p) == 2):
      p[0] = Node("and_expression", [p[1]])

   else:
      p[0] = Node("and_expression", [p[1], p[2],p[3]])


def p_equality_expression(p):
   '''equality_expression : relational_expression
								| equality_expression KW_EQUAL relational_expression
								| equality_expression KW_NEQUAL relational_expression'''


   if(len(p) == 2):
      p[0] = Node("equality_expression", [p[1]])

   else:
      p[0] = Node("equality_expression", [p[1], p[2],p[3]])

def p_relational_expression(p):
   '''relational_expression : shift_expression
								 | relational_expression KW_GREATER shift_expression
								 | relational_expression KW_LESS shift_expression
								 | relational_expression KW_GEQ shift_expression
								 | relational_expression KW_LEQ shift_expression'''



   if(len(p) == 2):
      p[0] = Node("equality_expression", [p[1]])

   else:
      p[0] = Node("equality_expression", [p[1], p[2],p[3]])

def p_shift_expression(p):
   '''shift_expression : additive_expression
									| shift_expression KW_LSHIFT additive_expression
									| shift_expression KW_RSHIFT additive_expression'''



   if(len(p) == 2):
      p[0] = Node("shift_expression", [p[1]])

   else:
      p[0] = Node("shift_expression", [p[1], p[2],p[3]])



def p_additive_expression(p):
   '''additive_expression : multiplicative_expression
								 | additive_expression KW_PLUS multiplicative_expression
								 | additive_expression KW_MINUS multiplicative_expression'''



   if(len(p) == 2):
      p[0] = Node("additive_expression", [p[1]])

   else:
      p[0] = Node("additive_expression", [p[1], p[2],p[3]])

def p_multiplicative_expression(p):
   '''multiplicative_expression : unary_expression

									 | multiplicative_expression KW_TIMES unary_expression
									 | multiplicative_expression KW_DIVIDE unary_expression
									 | multiplicative_expression KW_REMAINDER unary_expression'''



   if(len(p) == 2):
      p[0] = Node("multiplicative_expression", [p[1]])

   else:
      p[0] = Node("multiplicative_expression", [p[1], p[2],p[3]])

def p_unary_expression(p):
   '''unary_expression : PLUS unary_expression
							| KW_MINUS unary_expression
							| unary_expression_not_plus_minus'''




   if(len(p) == 2):
      p[0] = Node("unary_expression", [p[1]])

   else:
      p[0] = Node("unary_expression", [p[1], p[2]])


def p_unary_expression_not_plus_minus(p):
   '''unary_expression_not_plus_minus : base_variable_set
											 | KW_TILDA unary_expression
											 | KW_NOT unary_expression
											 | cast_expression'''




   if(len(p) == 2):
      p[0] = Node("unary_expression_not_plus_minus", [p[1]])

   else:
      p[0] = Node("unary_expression_not_plus_minus", [p[1], p[2]])


def p_base_variable_set(p):
   '''base_variable_set : variable_literal
						 | KW_LPAREN expression KW_RPAREN'''




   if(len(p) == 2):
      p[0] = Node("base_variable_set", [p[1]])

   else:
      p[0] = Node("base_variable_set", [p[1], p[2],p[3]])


def p_variable_literal(p):
   '''variable_literal : valid_variable | primary'''


   p[0] = Node("variable_literal", [p[1]])


def p_cast_expression(p):
   '''cast_expression : LPAREN primitive_type RPAREN unary_expression'''



   p[0] = Node("cast_expression", [p[1],p[2],p[3],p[4]])

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



   p[0] = Node("c_literal", [p[1]])

def p_int_float(p):
   '''int_float : KW_DOUBLE | KW_INT '''



   p[0] = Node("int_float", [p[1]])


def p_method_invocation(p):
   '''method_invocation : id LPAREN argument_list RPAREN '''



   p[0] = Node("method_invocation", [p[1],p[2],p[3],p[4]])


def p_argument_list(p):
   '''argument_list : expression
						| argument_list KW_COMMA expression'''




   if(len(p) == 2):
      p[0] = Node("argument_list", [p[1]])

   else:
      p[0] = Node("argument_list", [p[1], p[2],p[3]])

'''LOCAL VARIABLE DECLARATION'''

def p_modifier(p):
   ''' modifier : KW_protected | KW_private '''



   p[0] = Node("modifier", [p[1]])

def p_modifier_question(p):
   ''' modifier_question : modifier | empty '''



   p[0] = Node("modifier_question", [p[1]])

def p_declaration_keyword(p):
   '''declaration_keyword : KW_var | KW_val '''



   p[0] = Node("declaration_keyword", [p[1]])

def p_local_variable_declaration_statement(p):
   '''local_variable_declaration_statement : local_variable_declaration terminator '''



   p[0] = Node("local_variable_declaration_statement", [p[1],p[2]])

def p_terminator(p):
   '''terminator : KW_semi | KW_nl '''



   p[0] = Node("terminator", [p[1]])

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
										| variable_argument_list COMMA variable_declaration_initializer'''




   if(len(p) == 2):
      p[0] = Node("variable_argument_list", [p[1]])

   else:
      p[0] = Node("variable_argument_list", [p[1], p[2],p[3]])

def p_variable_argument_list(p):
   '''variable_declaration_body : identifiers type_opt KW_assignment  variable_declaration_initializer | KW_LPAREN variable_list KW_RPAREN KW_assignment KW_LPAREN variable_argument_list KW_RPAREN'''




   if(len(p) == 5):
      p[0] = Node("variable_argument_list", [p[1], p[2],p[3],p[4]])

   else:
      p[0] = Node("variable_argument_list", [p[1], p[2],p[3],p[4], p[5],p[6],p[7]])


def p_identifiers(p):
   ''' identifiers : identifiers KW_COMMA KW_IDENTIFIER | KW_IDENTIFIER'''




   if(len(p) == 2):
      p[0] = Node("identifiers", [p[1]])

   else:
      p[0] = Node("identifiers", [p[1], p[2],p[3]])




























def p_compile_unit(p):
   '''compilationUnit  : package_units_opt topStatSeq '''

   p[0]  = Node("compilationUnit", [p[1], p[2]])

def p_package_units_opt(p):
   '''package_units_opt : package_units | empty '''

   p[0] = Node("package_units_opt", [p[1]])

def p_package_units(p):
   '''package_units :  package_unit | package_units package_unit '''

   if(len(p) == 2):
      p[0] = Node("package_units", [p[1]])

   else:
      p[0] = Node("package_units", [p[1], p[2]])

def p_package_unit(p):
   '''package_unit : TOK_package qualid TOK_SEMICOLON'''

   leaf1 = create_children("TOK_package", p[1])
   leaf3 = create_children("TOK_SEMICOLON", p[3])
   p[0] = Node("package_unit", [leaf1, p[2], leaf3])

'''
packageObject
   : 'package' 'object' objectDef
   ;
'''

def p_package_object(p):
   '''packageObject : TOK_package TOK_object objectdef'''

   leaf1 = create_children("TOK_package",p[1])
   leaf2 = create_children("TOK_object",p[2])
   p[0] = Node("packageObject", [leaf1, leaf2, p[3]])


'''
packaging
   : 'package' qualId '{' topStatSeq '}'
   ;
'''

def p_packaging(p):
   '''packaging : TOK_package qualid TOK_LCUR topStatSeq TOK_RCUR '''

   leaf1 = create_children("TOK_package",p[1])
   leaf3 = create_children("TOK_LCUR",p[3])
   leaf5 = create_children("TOK_RCUR",p[5])
   p[0] = Node("packaging", [leaf1, p[2], leaf3, p[4], leaf5])

'''
topStat
   : (annotation)* modifier* tmplDef
   | import_
   | packaging
   | packageObject
   |
   ;
'''

def p_topStat(p):
   '''topStat : annotations_opt modifiers_opt tmplDef | import_ | packaging | packageObject '''

   if (len(p) == 4):
      p[0] = Node("topStat", [p[1], p[2], p[3]])
   else:
      p[0] = Node("topStat", p[1])

def p_annotations_opt(p):
   '''annotations_opt :  annotations | empty '''   

   p[0] = Node("annotations_opt", [p[1]])

def p_annotations(p):
   '''annotations : annotation | annotations annotation '''

   if(len(p) == 2):
      p[0] = Node("annotations", [p[1]])
   else:
      p[0] = Node("annotations", [p[1], p[2]])

def p_modifiers_opt(p):
   '''modifiers_opt : modifiers | empty '''

   p[0] = Node("modifiers_opt", [p[1]])

def p_modifiers(p):
   '''modifiers : modifier | modifiers modifier | empty '''

   if(len(p) == 2):
      p[0] = Node("modifiers", [p[1]])
   else:
      p[0] = Node("modifiers", [p[1], p[2]])


'''
topStatSeq
   : topStat (Semi topStat)*
   ;
'''
def p_topStatSeq(p):
   '''topstatSeq : topStat Semi_topStats_opt '''

   p[0] = Node("topstatSeq", [p[1], p[2]])

def p_Semi_topStats(p):
   '''SemitopStats_opt : SemitopStats | empty'''

   p[0] = Node("SemitopStats_opt", [p[1]])

def p_Semi_topStats(p):
   '''Semi_topStats : Semi_topStat | Semi_topStats Semi_topStat'''

   if(len(p) == 2):
      p[0] = Node("Semi_topStats", [p[1]])
   else:
      p[0] = Node("Semi_topStats", [p[1], p[2]])


def p_Semi_topStat(p):
   '''Semi_topStat : TOK_SEMICOLON topStat '''

   leaf1 = create_children("TOK_SEMICOLON",p[1])
   p[0] = Node("Semi_topStat", [leaf1, p[2]])


'''
selfInvocation
   : 'this' argumentExprs +
   ;
'''

def p_selfInvocation(p):
   '''selfInvocation : TOK_this argumentExprss'''

   leaf1 = create_children("TOK_this",p[1])
   p[0] = Node("selfInvocation", [leaf1, p[2]])

#defined here but not used in this rule
def p_argumentExprss_opt(p):
   '''argumentExprss_opt : argumentExprss | empty '''

   p[0] = Node("argumentExprss_opt", [p[1]])

def p_argumentExprss(p):
   '''argumentExprss : argumentExprs | argumentExprss argumentExprs'''
  
   if(len(p) == 2):
      p[0] = Node("argumentExprss", [p[1]])
   else:
      p[0] = Node("argumentExprss", [p[1], p[2]])



'''
constrBlock
   : '{' selfInvocation (Semi blockStat)* '}'
   ;
'''

def p_constrBlock(p):
   '''constrBlock : TOK_LCUR selfInvocation Semi_blockStats_opt TOK_RCUR '''

   leaf1 = create_children("TOK_LCUR",p[1])
   leaf4 = create_children("TOK_RCUR",p[4])
   p[0] = Node("constrBlock", [leaf1, p[2], p[3], leaf4])

def p_Semi_blockStats_opt(p):
   '''Semi_blockStats_opt : Semi_blockStats | empty'''

   p[0] = Node("Semi_blockStats_opt", [p[1]])

def p_Semi_blockStats(p):
   '''Semi_blockStats : Semi_blockStat | Semi_blockStats Semi_blockStat '''
   if(len(p) == 2):
      p[0] = Node("Semi_blockStats", [p[1]])
   else:
      p[0] = Node("Semi_blockStats", [p[1], p[2]])

def p_Semi_blockStat(p):
   '''Semi_blockStat : TOK_SEMICOLON blockStat'''

   leaf1 = create_children("TOK_SEMICOLON",p[1])
   p[0] = Node("Semi_blockStat", [leaf1, p[2]])


'''
constrExpr
   : selfInvocation
   | constrBlock
   ;
'''
def p_constrExpr(p):
   '''constrExpr : selfInvocation | constrBlock'''

   p[0] = Node("constrExpr", [p[1]])


'''
earlyDef
   : (annotation)* modifier* patVarDef
   ;
'''
#annotations and modifiers defined beforehand
def p_earlyDef(p):
   '''earlyDef : annotations_opt modifiers_opt patVarDef '''

   p[0] = Node("earlyDef", [p[1], p[2], p[3]])


'''
earlyDefs
   : '{' (earlyDef (Semi earlyDef)*)? '}' 'with'
   ;
'''

def p_earlyDefs(p):
   '''earlyDefs : TOK_LCUR empty TOK_RCUR TOK_with | TOK_LCUR earlyDef Semi_earlyDefs_opt TOK_RCUR TOK_with '''

   if(len(p) == 5):
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf3 = create_children("TOK_RCUR",p[3])
      leaf4 = create_children("TOK_with",p[4])
      p[0] = Node("earlyDefs", [leaf1, p[2], leaf3, leaf4])
   else:
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf4 = create_children("TOK_RCUR",p[4])
      leaf5 = create_children("TOK_with",p[5])
      p[0] = Node("earlyDefs", [leaf1, p[2], p[3], leaf4, leaf5])

def p_Semi_earlyDefs_opt(p):
   '''Semi_earlyDefs_opt : Semi_earlyDefs | empty '''

   p[0] = Node("Semi_earlyDefs_opt", [p[1]])

def p_Semi_earlyDefs(p):
   '''Semi_earlyDefs : Semi_earlyDef | Semi_earlyDefs Semi_earlyDef '''

   if(len(p) == 2):
      p[0] = Node("Semi_earlyDefs", [p[1]])
   else:
      p[0] = Node("Semi_earlyDefs", [p[1], p[2]])

def p_Semi_earlyDef(p):
   '''Semi_earlyDef : TOK _SEMICOLON earlyDef '''

   leaf1 = create_children("TOK _SEMICOLON",p[1])
   p[0] = Node("Semi_earlyDef", [leaf1, p[2]])


'''
constr
   : annotType argumentExprs*
   ;
'''

def p_constr(p):
   '''constr : annotType arguementsExprss_opt'''

   p[0] = Node("constr", [p[1], p[2]])

'''
traitParents
   : annotType ('with' annotType)*
   ;
'''
def p_traitParents(p):
   '''traitParents : annotType with_annotTypes_opt '''

   p[0] = Node("traitParents", [p[1], p[2]])

def p_with_annotTypes_opt(p):
   '''with_annotTypes_opt : with_annotTypes | empty '''

   p[0] = Node("with_annotTypes_opt", [p[1]])

def p_with_annotTypes(p):
   '''with_annotTypes : with_annotType | with_annotTypes with_annotType '''

   if(len(p) == 2):
      p[0] = Node("with_annotTypes", [p[1]])
   else:
      p[0] = Node("with_annotTypes", [p[1], p[2]])

def p_with_annotType(p):
   '''with_annotType : TOK_with annotType'''

   leaf1 = create_children("TOK_with",p[1])
   p[0] = Node("with_annotType", [leaf1, p[2]])

'''
classParents
   : constr ('with' annotType)*
   ;

'''
def p_classParents(p):
   '''classParents : constr with_annotTypes_opt'''

   p[0] = Node("classParents", [p[1], p[2]])


'''
traitTemplate
   : earlyDefs? traitParents templateBody?
   ;
'''
def p_traitTemplate(p):
   '''traitTemplate : traitParents | traitParents templateBody |  earlyDefs traitParents | earlyDefs traitParents templateBody'''

   if(len(p) == 2):
      p[0] = Node("traitTemplate", [p[1]])
   else if(len(p) == 3):
      p[0] = Node("traitTemplate", [p[1], p[2]])
   else:
      p[0] = Node("traitTemplate", [p[1], p[2], p[3]])

'''
classTemplate
   : earlyDefs? classParents templateBody?
   ;
'''
def p_classTemplate(p):
   '''classTemplate : classParents | classParents templateBody |  earlyDefs classParents | earlyDefs classParents templateBody'''

   if(len(p) == 2):
      p[0] = Node("classTemplate", [p[1]])
   else if(len(p) == 3):
      p[0] = Node("classTemplate", [p[1], p[2]])
   else:
      p[0] = Node("classTemplate", [p[1], p[2], p[3]])

'''
traitTemplateOpt
   : 'extends' traitTemplate
   | ('extends'? templateBody)?
   ;
'''
def p_traitTemplateOpt(p):
   '''traitTemplateOpt : TOK_extends traitTemplate | TOK_extends templateBody | templateBody | empty'''
   if(len(p) == 3):
      leaf1 = create_children("TOK_extends",p[1])
      p[0] = Node("traitTemplateOpt", [leaf1, p[2]])
   else:
      p[0] = Node("traitTemplateOpt", [p[1]])

'''
classTemplateOpt
   : 'extends' classTemplate
   | ('extends'? templateBody)?
   ;
'''
def p_classTemplateOpt(p):
   ''' classTemplateOpt : TOK_extends classTemplate | TOK_extends templateBody | templateBody | empty'''

   if(len(p) == 3):
      leaf1 = create_children("TOK_extends",p[1])
      p[0] = Node("classTemplateOpt", [leaf1, p[2]])
   else:
      p[0] = Node("classTemplateOpt", [p[1]])

'''
objectDef
   : Id classTemplateOpt
   ;
'''

def p_objectDef(p):
   '''objectDef : Id classTemplateOpt'''

   p[0] = Node("objectDef", [p[1], p[2]])

'''
traitDef
   : Id typeParamClause? traitTemplateOpt
   ;
'''
def p_traitDef(p):
   '''traitDef : Id traitTemplateOpt | Id typeParamClause traitTemplateOpt'''

   if(len(p) == 3):
      p[0] = Node("traitDef", [p[1], p[2]])
   else:
      p[0] = Node("traitDef", [p[1], p[2], p[3]])

'''
classDef
   : Id typeParamClause? constrAnnotation* accessModifier? classParamClauses classTemplateOpt
   ;
'''

def p_classDef(p):
   '''classDef : Id constrAnnotations_opt classParamClauses classTemplateOpt
               | Id constrAnnotations_opt accessModifier classParamClauses classTemplateOpt 
               | Id typeParamClause constrAnnotations_opt  classParamClauses classTemplateOpt 
               | Id typeParamClause constrAnnotations_opt accessModifier classParamClauses classTemplateOpt '''

   if(len(p) == 5):
      p[0] = Node("classDef", [p[1], p[2], p[3], p[4]])
   else if(len(p) == 6):
      p[0] = Node("classDef", [p[1], p[2], p[3], p[4], p[5]])
   else:
      p[0] = Node("classDef", [p[1], p[2], p[3], p[4], p[5], p[6]])


def p_constrAnnotations_opt(p):
   '''constrAnnotations_opt : constrAnnotations | empty '''
   p[0] = Node("constrAnnotations_opt", [p[1]])

def p_constrAnnotations(p):
   '''constrAnnotations : constrAnnotation | constrAnnotations constrAnnotation '''
   if(len(p) == 2):
      p[0] = Node("constrAnnotations", [p[1]])
   else:
      p[0] = Node("constrAnnotations", [p[1], p[2]])

'''
tmplDef
   : 'case'? 'class' classDef
   | 'case' 'object' objectDef
   | 'trait' traitDef
   ;
'''
#defined in new way. Please check

def p_tmplDef(p):
   '''tmplDef    : TOK_class classDef | TOK_case TOK_class classDef  | TOK_case TOK_object objectDef | TOK_trait traitDef '''
   if(p[1] == 'class'):
      leaf1 = create_children("TOK_class",p[1])
      p[0] = Node("tmplDef", [leaf1, p[2]])
   else if(p[1] == 'trait'):
      leaf1 = create_children("TOK_trait",p[1])
      p[0] = Node("tmplDef", [leaf1, p[2]])
   else if(p[2] == 'class'):
      leaf1 = create_children("TOK_case",p[1])
      leaf2 = create_children("TOK_class",p[2])
      p[0] = Node("tmplDef", [leaf1, leaf2, p[3]])
   else:
      leaf1 = create_children("TOK_case",p[1])
      leaf2 = create_children("TOK_object",p[2])
      p[0] = Node("tmplDef", [p[1], p[2], p[3]])


'''
typeDef
   : Id typeParamClause? '=' type
   ;
'''
def p_typeDef(p):
   '''typeDef :  Id TOK_ASSIGN type | Id typeParamClause TOK_ASSIGN type '''

   if(len(p) == 4):
      leaf2 = create_children("TOK_ASSIGN",p[2])
      p[0] = Node("typeDef", [p[1], leaf2, p[3]])
    else:
      leaf3 = create_children("TOK_ASSIGN",p[3])
      p[0] = Node("typeDef", [p[1], p[2], leaf3, p[4]])

'''
funDef
   : funSig (':' type)? '=' expr
   | funSig '{' block '}'
   | 'this' paramClause paramClauses ('=' constrExpr | constrBlock)
   ;
'''

def p_funDef(p):
   '''funDef : funSig TOK_ASSIGN expr
              | funSig TOK_LCUR block TOK_RCUR 
              | TOK_this paramClause paramClauses constrBlock
              | funSig TOK_COLON type TOK_ASSIGN expr   
              | TOK_this paramClause paramClauses TOK_ASSIGN constrExpr '''

   if(len(p) == 4):
      leaf2 = create_children("TOK_ASSIGN",p[2])
      p[0] = Node("funDef", [p[1], leaf2, p[3]])
   else if(len(p) == 5):
      if(p[2] == '{'):
         leaf2 = create_children("TOK_LCUR",p[2])
         leaf4 = create_children("TOK_RCUR",p[4])
         p[0] = Node("funDef", [p[1], leaf2, p[3], leaf4])
      else:
         leaf1 = create_children("TOK_this",p[1])
         p[0] = Node("funDef", [leaf1, p[2], p[3], p[4]])

   else:
      if(p[2] == ':'):
         leaf2 = create_children("TOK_COLON",p[2])
         leaf4 = create_children("TOK_ASSIGN",p[4])
         p[0] = Node("funDef", [p[1], leaf2, p[3], leaf4, p[5]])
      else:
         leaf1 = create_children("TOK_this",p[1])
         leaf4 = create_children("TOK_ASSIGN",p[4])
         p[0] = Node("funDef", [leaf1, p[2], p[3], leaf4, p[5]])

'''
varDef
   : patDef
   | ids ':' type '=' '_'
   ;
'''

def p_varDef(p):
   '''varDef   : patDef | ids TOK_COLON type TOK_ASSIGN TOK_UNDERSCORE ''' 

   if(len(p) == 2):
      p[0] = Node("varDef", [p[1]])
   else:
      leaf2 = create_children("TOK_COLON",p[2])
      leaf4 = create_children("TOK_ASSIGN",p[4])
      leaf5 = create_children("TOK_UNDERSCORE",p[5])
      p[0] = Node("varDef", [p[1], leaf2, p[3], leaf4, leaf5])

'''
patDef
   : pattern2 (',' pattern2)* (':' type)* '=' expr
   ;
'''
def p_patDef(p):
   '''patDef : pattern2 TOK_COMMA_pattern2s_opt TOK_COLON_types_opt TOK_ASSIGN expr '''

   leaf4 = create_children("TOK_ASSIGN",p[4])
   p[0] = Node("patDef", [p[1], p[2], p[3], leaf4])

def p_TOK_COMMA_pattern2s_opt(p):
   '''TOK_COMMA_pattern2s_opt : TOK_COMMA_pattern2s | empty '''

   p[0] = Node("TOK_COMMA_pattern2s_opt", [p[1]])

def p_TOK_COMMA_pattern2s(p):
   '''TOK_COMMA_pattern2s : TOK_COMMA_pattern2 | TOK_COMMA_pattern2s TOK_COMMA_pattern2 '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_pattern2s", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_pattern2s", [p[1], p[2]])

def TOK_COMMA_pattern2(p):
   '''TOK_COMMA_pattern2 : TOK_COMMA pattern2 '''

   leaf1 = create_children("TOK_COMMA",p[1])
   p[0] = Node("TOK_COMMA_pattern2", [leaf1, p[2]])

def p_TOK_COLON_types_opt(p):
   '''TOK_COLON_types_opt : TOK_COLON_types | empty '''

   p[0] = Node("TOK_COLON_types_opt", [p[1]])

def p_TOK_COLON_types(p):
   '''TOK_COLON_types : TOK_COLON_type | TOK_COLON_types TOK_COLON_type '''

   if(len(p) == 2):
      p[0] = Node("TOK_COLON_types", [p[1]])
    else:
      p[0] = Node("TOK_COLON_types", [p[1], p[2]])

def p_TOK_COLON_type(p):
   '''TOK_COLON_type : TOK_COLON type '''

   leaf1 = create_children("TOK_COLON",p[1])
   p[0] = Node("TOK_COLON_type", [p[1], p[2]])


#Note : 'Def' in the below rule was 'def' but has been changed as def is keyword for python
'''
Def
   : patVarDef
   | 'def' funDef
   | 'type' typeDef
   | tmplDef
   ;
'''

def p_Def(p):
   '''Def: patVarDef | TOK_def funDef   | TOK_type typeDef   | tmplDef '''

   if(len(p) == 2):
      p[0] = Node("Def", [p[1]])
    else:
      if(p[1] == 'def'):
         leaf1 = create_children("TOK_def",p[1])
         p[0] = Node("Def", [leaf1, p[2]])
      else:
         leaf1 = create_children("TOK_type",p[1])
         p[0] = Node("Def", [leaf1, p[2]])


'''
patVarDef
   : 'val' patDef
   | 'var' varDef
   ;
'''
def p_patVarDef(p):
   '''patVarDef : TOK_val patDef | TOK_var varDef '''
   if(p[1] == 'val'):
      leaf1 = create_children("TOK_val",p[1])
      p[0] = Node("patVarDef", [leaf1, p[2]])
   else:
      leaf1 = create_children("TOK_var",p[1])
      p[0] = Node("patVarDef", [leaf1, p[2]])

'''
typeDcl
   : Id typeParamClause? ('>:' type)? ('<:' type)?
   ;
'''
def p_typeDcl(p):
   '''typeDcl : Id 
                    | Id typeParamClause   
                    | Id TOK_LT_COLON type 
                    | Id TOK_GT_COLON type  
                    | Id typeParamClause TOK_LT_COLON type 
                    | Id typeParamClause TOK_GT_COLON type 
                    | Id TOK_GT_COLON type TOK_LT_COLON type 
                    | Id typeParamClause TOK_GT_COLON type TOK_LT_COLON type '''

   if(len(p) == 2):
      p[0] = Node("typeDcl", [p[1]])

   else if(len(p) == 3):
      p[0] = Node("typeDcl", [p[1], p[2]])

   else if(len(p) == 4):
         if(p[2] == '>:'):
            leaf2 = create_children("TOK_LT_COLON",p[2])
            p[0] = Node("typeDcl", [p[1], leaf2, p[3]])
         else:
            leaf2 = create_children("TOK_GT_COLON",p[2])
            p[0] = Node("typeDcl", [p[1], leaf2, p[3]])

   else if(len(p) == 5):
      if(p[3] == '>:'):
         leaf3 = create_children("TOK_LT_COLON",p[3])
         p[0] = Node("typeDcl", [p[1], p[2], leaf3, p[4]])
      else:
         leaf3 = create_children("TOK_LT_COLON",p[3])
         p[0] = Node("typeDcl", [p[1], p[2], leaf3, p[4]])

   else if (len(p) == 6):
      leaf2 = create_children("TOK_GT_COLON",p[2])
      leaf4 = create_children("TOK_LT_COLON",p[4])
      p[0] = Node("typeDcl", [p[1], leaf2, p[3], leaf4, p[5]])
   else if (len(p) == 7):
      leaf3 = create_children("TOK_GT_COLON",p[3])
      leaf5 = create_children("TOK_LT_COLON",p[5])
      p[0] = Node("typeDcl", [p[1], p[2], leaf3, p[4], leaf5, p[6]])

'''
funSig
   : Id funTypeParamClause? paramClauses
'''

def p_funSig(p):
   '''funSig : Id paramClauses | Id funTypeParamClause paramClauses '''

   if(len(p) == 3):
      p[0] = Node("funSig", [p[1], p[2]])
    else:
      p[0] = Node("funSig", [p[1], p[2], p[3]])

'''
funDcl
   : funSig (':' type)?
   ;
'''

def p_funDcl(p):
   '''funDcl  : funSig | funSig TOK_COLON_type '''
   if(len(p) == 2):
      p[0] = Node("funDcl", [p[1]])
    else:
      leaf2 = create_children("TOK_COLON",p[2])
      p[0] = Node("funDcl", [p[1], leaf2])


'''
varDcl
   : ids ':' type
   ;
'''

def p_varDcl(p):
   '''varDcl : ids TOK_COLON type '''
   leaf2 = create_children("TOK_COLON",p[2])
   p[0] = Node("varDcl", [p[1], leaf2, p[3]])


'''
valDcl
   : ids ':' type
   ;
'''

def p_valDcl(p):
   '''valDcl : ids TOK_COLON type'''
   leaf2 = create_children("TOK_COLON",p[2])
   p[0] = Node("valDcl", [p[1], leaf2, p[3]])

'''
dcl
   : 'val' valDcl
   | 'var' varDcl
   | 'def' funDcl
   | 'type' typeDcl
   ;
'''
def p_dcl(p):
   '''dcl  : TOK_val valDcl  | TOK_var varDcl   | TOK_def funDcl  | TOK_type typeDcl '''
   if(p[1] == 'val'):
      leaf1 = create_children("TOK_val",p[1])
      p[0] = Node("dcl", [leaf1, p[2]])
   else if(p[1] == 'var'):
      leaf1 = create_children("TOK_var",p[1])
      p[0] = Node("dcl", [leaf1, p[2]])
   else if(p[2] == 'def'):
      leaf1 = create_children("TOK_def",p[1])
      p[0] = Node("dcl", [leaf1, p[2]])
   else:
      leaf1 = create_children("TOK_type",p[1])
      p[0] = Node("TOK_type", [p[1]])


'''
importSelector
   : Id ('=>' Id | '=>' '_')
   ;
'''
def p_importSelector(p):
	'''importSelector  : Id TOK_EQ_GT TOK_UNDERSCORE | Id TOK_EQ_GT Id '''

   if(p[3] == '_'):
      leaf2 = create_children("TOK_EQ_GT",p[2])
      leaf3 = create_children("TOK_UNDERSCORE",p[3])
      p[0] = Node("importSelector", [p[1], p[2], p[3]])
   else:
      leaf2 = create_children("TOK_EQ_GT",p[2])
      p[0] = Node("importSelector", [p[1], leaf2, p[3]])


'''
importSelectors
   : '{' (importSelector ',')* (importSelector | '_') '}'
   ;
'''

def p_importSelectors(p):
	'''importSelectors : TOK_LCUR importSelector_TOK_COMMAs_opt importSelector TOK_RCUR 
                       | TOK_LCUR importSelector_TOK_COMMAs_opt TOK_UNDERSCORE TOK_RCUR'''
   if(p[3] == '_'):
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf3 = create_children("TOK_UNDERSCORE",p[3])
      leaf4 = create_children("TOK_RCUR",p[4])
      p[0] = Node("importSelectors", [leaf1, p[2], leaf3, leaf4])
   else:
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf4 = create_children("TOK_RCUR",p[4])
      p[0] = Node("importSelectors", [leaf1, p[2], p[3], leaf4])


def p_importSelector_TOK_COMMAs_opt(p):
	'''importSelector_TOK_COMMAs_opt : importSelector_TOK_COMMAs | empty '''

   p[0] = Node("importSelector_TOK_COMMAs_opt", [p[1]])

def importSelector_TOK_COMMAs(p);
	'''importSelector_TOK_COMMAs : importSelector_TOK_COMMA 
                                | importSelector_TOK_COMMAs importSelector_TOK_COMMA '''

   if(len(p) == 2):
      p[0] = Node("importSelector_TOK_COMMAs", [p[1]])
    else:
      p[0] = Node("importSelector_TOK_COMMAs", [p[1], p[2]])

def importSelector_TOK_COMMA(p):
	'''importSelector_TOK_COMMA : importSelector TOK_COMMA'''

   leaf2 = create_children("TOK_COMMA",p[2])
   p[0] = Node("importSelector_TOK_COMMA", [p[1], leaf2])

'''
importExpr
   : stableId '.' (Id | '_' | importSelectors)
   ;
'''

def p_importExpr(p):
	'''importExpr  : stableId TOK_DOT Id | stableId TOK_DOT TOK_UNDERSCORE  | stableId TOK_DOT importSelectors '''

   leaf2 = create_children("TOK_DOT",p[2])
   if(p[3] == '_'):
      leaf3 = create_children("TOK_UNDERSCORE",p[3])
      p[0] = Node("importExpr", [p[1], leaf2, leaf3])
   else:
      p[0] = Node("importExpr", [p[1], leaf2, p[3]])

'''
import_
   : 'import' importExpr (',' importExpr)*
   ;
'''

def p_import_(p);
	'''import_ : TOK_import importExpr TOK_COMMA_importExprs_opt '''
   leaf1 = create_children("TOK_import",p[1])
   p[0] = Node("import_", [leaf1, p[2], p[3]])

def p_TOK_COMMA_importExprs_opt(p):
	'''TOK_COMMA_importExprs_opt : TOK_COMMA_importExprs | empty '''
   p[0] = Node("TOK_COMMA_importExprs_opt", [p[1]])

def p_TOK_COMMA_importExprs(p):
	'''TOK_COMMA_importExprs : TOK_COMMA_importExpr | TOK_COMMA_importExprs TOK_COMMA_importExpr '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_importExprs", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_importExprs", [p[1], p[2]])

def p_TOK_COMMA_importExpr(p):
	'''TOK_COMMA_importExpr : TOK_COMMA importExpr'''

   leaf1 = create_children("TOK_COMMA",p[1])
   p[0] = Node("TOK_COMMA_importExpr", [leaf1, p[2]])


'''
selfType
   : Id (':' type)? '=>'
   | 'this' ':' type '=>'
   ;
'''

def p_selfType(p):
	'''selfType : Id TOK_EQ_GT | Id  TOK_COLON type TOK_EQ_GT | TOK_this TOK_COLON type TOK_EQ_GT'''

   if(len(p) == 3):
      leaf2 = create_children("TOK_EQ_GT",p[2])
      p[0] = Node("selfType", [p[1], p[2]])
   else:
      if(p[1] == 'this'):
         leaf1 = create_children("TOK_this",p[1])
         leaf2 = create_children("TOK_COLON",p[2])
         leaf4 = create_children("TOK_EQ_GT",p[4])
         p[0] = Node("selfType", [leaf1, leaf2, p[3], leaf4])
      else:
         leaf2 = create_children("TOK_COLON",p[2])
         leaf4 = create_children("TOK_EQ_GT",p[4])
         p[0] = Node("selfType", [p[1], leaf2, p[3], leaf4])



'''
templateStat
   : import_
   | (annotation)* modifier* def
   | (annotation)* modifier* dcl
   | expr
   |
   ;
'''
def p_templateStat(p):
	'''templateStat : import_  | annotations_opt modifiers_opt def  | annotations_opt modifiers_opt dcl | expr | empty '''

   if(len(p) == 2):
      p[0] = Node("templateStat", [p[1]])
    else:
      p[0] = Node("templateStat", [p[1], p[2], p[3]])

'''
templateBody
   : '{' selfType? templateStat (Semi templateStat)* '}'
   ;
'''
def p_templateBody(p):
   '''templateBody : TOK_LCUR templateStat TOK_SEMICOLON_templateStats_opt TOK_RCUR 
                   | TOK_LCUR selfType templateStat TOK_SEMICOLON_templateStats_opt TOK_RCUR '''

   if(len(p) == 5):
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf4 = create_children("TOK_RCUR",p[4])
      p[0] = Node("templateBody", [leaf1, p[2], p[3], leaf4])
    else:
      leaf1 = create_children("TOK_LCUR",p[1])
      leaf5 = create_children("TOK_RCUR",p[5])
      p[0] = Node("templateBody", [leaf1, p[2], p[3], p[4], leaf5])

def p_TOK_SEMICOLON_templateStats_opt(p):
   '''TOK_SEMICOLON_templateStats_opt : TOK_SEMICOLON_templateStats | empty '''

   p[0] = Node("TOK_SEMICOLON_templateStats_opt", [p[1]])

def p_TOK_SEMICOLON_templateStats(p):
   '''TOK_SEMICOLON_templateStats : TOK_SEMICOLON_templateStat | TOK_SEMICOLON_templateStats TOK_SEMICOLON_templateStat '''

   if(len(p) == 2):
      p[0] = Node("TOK_SEMICOLON_templateStats", [p[1]])
    else:
      p[0] = Node("TOK_SEMICOLON_templateStats", [p[1], p[2]])

def p_TOK_SEMICOLON_templateStat(p):
   '''TOK_SEMICOLON_templateStat : TOK_SEMICOLON templateStat '''

   leaf1 = create_children("TOK_SEMICOLON",p[1])
   p[0] = Node("TOK_SEMICOLON_templateStat", [leaf1, p[2]])


'''
constrAnnotation
   : '@' simpleType argumentExprs
   ;
'''

def p_constrAnnotation(p):
	'''constrAnnotation : TOK_AT simpleType argumentExprs '''
	leaf1 = create_children("TOK_AT",p[1])
   p[0] = Node("constrAnnotation", [leaf1, p[2], p[3]])

'''
annotation
   : '@' simpleType argumentExprs*
   ;
'''

def p_annotation(p):
	'''annotation : TOK_AT simpleType argumentExprss_opt :'''

   leaf1 = create_children("TOK_AT",p[1])
   p[0] = Node("annotation", [leaf1, p[2], p[3]])

'''
accessQualifier
   : '[' (Id | 'this') ']'
   ;
'''

def p_accessQualifier(p):
	'''accessQualifier  : TOK_LSQB Id TOK_RSQB | TOK_LSQB  TOK_this TOK_RSQB '''

   leaf1 = create_children("TOK_LSQB",p[1])
   leaf3 = create_children("TOK_RSQB",p[3])

   if(p[2] == 'this'):
      leaf2 = create_children("TOK_this",p[2])
      p[0] = Node("accessQualifier", [leaf1, leaf2, leaf3])
   else:
      p[0] = Node("accessQualifier", [leaf1, p[2], leaf3])

'''
accessModifier
   : ('private' | 'protected') accessQualifier?
   ;
'''

def p_accessModifier(p);
	'''accessModifier : TOK_private | TOK_private accessQualifier | TOK_protected | TOK_protected accessQualifier '''

   if(len(p) == 2):
      if(p[1] == 'private'):
         leaf1 = create_children("TOK_private",p[1])
         p[0] = Node("accessModifier", [leaf1])
      else:
         leaf1 = create_children("TOK_protected",p[1])
         p[0] = Node("accessModifier", [leaf1])
    else:
      if(p[1] == 'private'):
         leaf1 = create_children("TOK_private",p[1])
         p[0] = Node("accessModifier", [leaf1, p[2]])
      else:
         leaf1 = create_children("TOK_protected",p[1])
         p[0] = Node("accessModifier", [leaf1, p[2]])

'''
localModifier
   : 'abstract'
   | 'final'
   | 'sealed'
   | 'implicit'
   | 'lazy'
   ;
'''

def p_localModifier(p):
	'''localModifier : TOK_abstract   | TOK_final   | TOK_sealed   | TOK_implicit  | TOK_lazy	'''
   if(p[1] == 'abstract'):
      leaf1 = create_children("TOK_abstract",p[1])
      p[0] = Node("localModifier", [leaf1])
   else if(p[1] == 'final'):
      leaf1 = create_children("TOK_final",p[1])
      p[0] = Node("localModifier", [leaf1])
   else if(p[1] == 'sealed'):
      leaf1 = create_children("TOK_sealed",p[1])
      p[0] = Node("localModifier", [leaf1])
   else if(p[1] == 'implicit'):
      leaf1 = create_children("TOK_implicit",p[1])
      p[0] = Node("localModifier", [leaf1])
   else:
      leaf1 = create_children("TOK_lazy",p[1])
      p[0] = Node("localModifier", [leaf1])

'''
modifier
   : localModifier
   | accessModifier
   | 'override'
   ;
'''

def p_modifier(p):
   '''modifier : localModifier | accessModifier | TOK_override '''
   if(p[1] == 'override'):
      leaf1 = create_children("TOK_override",p[1])
      p[0] = Node("modifier", [leaf1])
   else:
      p[0] = Node("modifier", [p[1]])

'''
binding
   : (Id | '_') (':' type)?
   ;
'''
def p_binding(p):
   '''binding   : TOK_UNDERSCORE | Id | Id TOK_COLON_type | TOK_UNDERSCORE TOK_COLON_type  '''

   if(len(p) == 2):
      if(p[1] == '_'):
         leaf1 = create_children("TOK_UNDERSCORE",p[1])
         p[0] = Node("binding", [leaf1])
      else:        
         p[0] = Node("binding", [p[1]])

    else:
      if(p[1] == '_'):
         leaf1 = create_children("TOK_UNDERSCORE",p[1])
         p[0] = Node("binding", [leaf1, p[2]])
      else:
         p[0] = Node("binding", [p[1], p[2]])

'''
bindings
   : '(' binding (',' binding)* ')'
   ;
'''   
def p_bindings(p):
   '''bindings : TOK_LPAREN binding TOK_COMMA_bindings_opt TOK_RPAREN '''

   p[0] = Node("bindings", [p[1], p[2], p[3], p[4]])

def p_TOK_COMMA_bindings_opt(p):
   '''TOK_COMMA_bindings_opt : TOK_COMMA_bindings | empty '''

   p[0] = Node("TOK_COMMA_bindings_opt", [p[1]])

def p_TOK_COMMA_bindings(p):
   '''TOK_COMMA_bindings : TOK_COMMA_binding | TOK_COMMA_bindings TOK_COMMA_binding '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_bindings", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_bindings", [p[1], p[2]])

def p_TOK_COMMA_binding(p):
   '''TOK_COMMA_binding : TOK_COMMA bindings '''

   p[0] = Node("TOK_COMMA_binding", [p[1], p[2]])

'''
classParam
   : annotation* modifier* ('val' | 'var')? Id ':' paramType ('=' expr)?
   ;
'''

def p_classParam(p):
   '''classParam   : TOK_annotations_opt TOK_modifiers_opt Id TOK_COLON paramType 
         | TOK_annotations_opt TOK_modifiers_opt Id TOK_COLON paramType TOK_ASSIGN expr 
         | TOK_annotations_opt TOK_modifiers_opt TOK_val Id TOK_COLON paramType 
         | TOK_annotations_opt TOK_modifiers_opt TOK_var Id TOK_COLON paramType 
         | TOK_annotations_opt TOK_modifiers_opt TOK_val Id TOK_COLON paramType TOK_ASSIGN expr 
         | TOK_annotations_opt TOK_modifiers_opt TOK_var Id TOK_COLON paramType TOK_ASSIGN expr '''

   if(len(p) == 6):
      p[0] = Node("classParam", [p[1], p[2], p[3], p[4], p[5]])
   else if(len(p) == 8):
      p[0] = Node("classParam", [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])
   else:
      p[0] = Node("classParam", [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]])

'''
classParams
   : classParam (',' classParam)*
   ;
'''
def p_classParams(p):
   '''classParams   : classParam TOK_COMMA_classParams_opt '''

   p[0] = Node("classParams", [p[1], p[2]])

def p_TOK_COMMA_classParams_opt(p):
   '''TOK_COMMA_classParams_opt : TOK_COMMA_classParams | empty'''

   p[0] = Node("TOK_COMMA_classParams_opt", [p[1]])

def p_TOK_COMMA_classParams(p):
   '''TOK_COMMA_classParams : TOK_COMMA_classParam | TOK_COMMA_classParams TOK_COMMA_classParam '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_classParams", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_classParams", [p[1], p[2]])

def p_TOK_COMMA_classParam(p):
   '''TOK_COMMA_classParams : TOK_COMMA classParams'''

   p[0] = Node("TOK_COMMA_classParams", [p[1], p[2]])
    

'''
classParamClause
   : '(' classParams? ')'
   ;
'''

def p_classParamClause(p):
   '''classParamClause   : TOK_LPAREN TOK_RPAREN | TOK_LPAREN classParams TOK_RPAREN  '''

   if(len(p) == 3):
      p[0] = Node("classParamClause", [p[1], p[2]])
    else:
      p[0] = Node("classParamClause", [p[1], p[2], p[3]])

'''
classParamClauses
   : classParamClause* ('(' 'implicit' classParams ')')?
   ;
'''

def p_classParamClauses(p):
   '''classParamClauses  : classParamClauses_opt | classParamClauses_opt TOK_LPAREN TOK_implicit classParams TOK_RPAREN '''

   if(len(p) == 2):
      p[0] = Node("classParamClauses", [p[1]])
    else:
      p[0] = Node("classParamClauses", [p[1], p[2], p[3], p[4], p[5]])

def p_classParamClauses_opt(p):
   '''classParamClauses_opt : classParamClauses | empty '''

   p[0] = Node("classParamClauses_opt", [p[1]])

def p_classParamClauses(p):
   '''classParamClauses : classParamClause | classParamClauses classParamClause '''

   if(len(p) == 2):
      p[0] = Node("classParamClauses", [p[1]])
    else:
      p[0] = Node("classParamClauses", [p[1], p[2]])

'''
paramType
   : type
   | '=>' type
   | type '*'
   ;
'''
def p_paramType(p):
   '''paramType : type | TOK_EQ_GT type   | type TOK_STAR'''

   if(len(p) == 2):
      p[0] = Node("paramType", [p[1]])
    else:
      p[0] = Node("paramType", [p[1], p[2]])



'''
param
   : annotation* Id (':' paramType)? ('=' expr)?
   ;
'''
def p_param(p):
   '''param : annotations_opt Id | annotations_opt Id TOK_ASSIGN expr 
            | annotations_opt Id TOK_COLON paramType  | annotations_opt Id TOK_COLON paramType TOK_ASSIGN expr '''

   if(len(p) == 3):
      p[0] = Node("param", [p[1], p[2]])
   else if(len(p) == 5):
      p[0] = Node("param", [p[1], p[2], p[3], p[4]])
   else:
      p[0] = Node("param", [p[1], p[2], p[3], p[4], p[5], p[6]])

   
def p_TOK_COLON_paramTypes_opt(p):
   '''TOK_COLON_paramTypes_opt : TOK_COLON_paramTypes | empty '''

   p[0] = Node("TOK_COLON_paramTypes_opt", [p[1]])

def p_TOK_COLON_paramTypes(p):
   '''TOK_COLON_paramTypes : TOK_COLON_paramType | TOK_COLON_paramTypes TOK_COLON_paramType '''

   if(len(p) == 2):
      p[0] = Node("TOK_COLON_paramTypes", [p[1]])
    else:
      p[0] = Node("TOK_COLON_paramTypes", [p[1], p[2]])

def p_TOK_COLON_paramType(p):
   '''TOK_COLON_paramType : TOK_COLON paramTypes '''

   p[0] = Node("TOK_COLON_paramType", [p[1], p[2]])


'''
params
   : param (',' param)*
   ;
'''

def p_params(p):
   '''params : param TOK_COMMA_params_opt  '''

   p[0] = Node("params", [p[1], p[2]])
   

def p_TOK_COMMA_params_opt(p):
   '''TOK_COMMA_params_opt : TOK_COMMA_params | empty '''

   p[0] = Node("TOK_COMMA_params_opt", [p[1]])

def p_TOK_COMMA_params(p):
   '''TOK_COMMA_params : TOK_COMMA_param | TOK_COMMA_params TOK_COMMA_param '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_params", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_params", [p[1], p[2]])

def p_TOK_COMMA_param(p):
   '''TOK_COMMA_param : TOK_COLON param'''

   p[0] = Node("TOK_COMMA_param", [p[1], p[2]])


'''
paramClause
   : '(' params? ')'
   ;
'''
def p_paramClause(p):
   '''paramClause : TOK_LPAREN TOK_RPAREN | TOK_LPAREN params TOK_RPAREN'''

   if(len(p) == 3):
      p[0] = Node("paramClause", [p[1], p[2]])
    else:
      p[0] = Node("paramClause", [p[1], p[2], p[3]])
   
'''
paramClauses
   : paramClause* ('(' 'implicit' params ')')?
   ;
'''
def p_paramClauses(p):
   '''paramClauses : paramClauses_opt | paramClauses_opt TOK_LPAREN TOK_implicit params TOK_RPAREN  '''

   if(len(p) == 2):
      p[0] = Node("paramClauses", [p[1]])
    else:
      p[0] = Node("paramClauses", [p[1], p[2], p[3], p[4], p[5]])


'''
literal
   : '-'? IntegerLiteral
   | '-'? FloatingPointLiteral
   | BooleanLiteral
   | CharacterLiteral
   | StringLiteral
   | SymbolLiteral
   | 'null'
   ;
'''
def p_literal(p):
   '''literal : TOK_MINUS IntegerLiteral | IntegerLiteral | FloatingPointLiteral 
   | TOK_MINUS FloatingPointLiteral   | BooleanLiteral 
   | CharacterLiteral | StringLiteral | SymbolLiteral | TOK_null'''

   if(len(p) == 2):
      p[0] = Node("literal", [p[1]])
    else:
      p[0] = Node("literal", [p[1], p[2]])

'''
qualId
   : Id ('.' Id)*
   ;
'''
def p_qualId(p):
   '''qualId   : Id TOK_DOT_Ids_opt '''

   p[0] = Node("qualId", [p[1]])

def p_TOK_DOT_Ids_opt(p):
   '''TOK_DOT_Ids_opt : TOK_DOT_Ids | empty '''

   p[0] = Node("TOK_DOT_Ids_opt", [p[1]])

def p_TOK_DOT_Ids(p):
   '''TOK_DOT_Ids : TOK_DOT_Id | TOK_DOT_Ids TOK_DOT_Id '''

   if(len(p) == 2):
      p[0] = Node("TOK_DOT_Ids", [p[1]])
    else:
      p[0] = Node("TOK_DOT_Ids", [p[1], p[2]])

def TOK_DOT_Id(p):
   '''TOK_DOT_Id : TOK_DOT Id '''

   p[0] = Node("TOK_DOT_Id", [p[1], p[2]])


'''
ids
   : Id (',' Id)*
   ;
'''
def p_ids(p):
   '''ids : Id TOK_COMMA_Ids_opt '''

   p[0] = Node("ids", [p[1], p[2]])

def p_TOK_COMMA_Ids_opt(p):
   '''TOK_COMMA_Ids_opt : TOK_COMMA_Ids | empty '''

   p[0] = Node("TOK_COMMA_Ids_opt", [p[1]])

def p_TOK_COMMA_Ids(p):
   '''TOK_COMMA_Ids : TOK_COMMA_Id | TOK_COMMA_Ids TOK_COMMA_Id '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_Ids", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_Ids", [p[1], p[2]])

def TOK_COMMA_Id(p):
   '''TOK_COMMA_Id : TOK_COMMA Id '''

   p[0] = Node("TOK_COMMA_Id", [p[1], p[2]])

   
'''
stableId
   : (Id | (Id '.')? 'this') '.' Id
   | (Id '.')? 'super' classQualifier? '.' Id
   ;
'''
def p_stableId(p):
   '''stableId  : Id TOK_DOT Id   | TOK_this TOK_DOT Id | Id TOK_DOT TOK_this TOK_DOT Id
      | TOK_super TOK_DOT Id | TOK_super classQualifier TOK_DOT Id
      | Id TOK_DOT TOK_super TOK_DOT Id | Id TOK_DOT TOK_super classQualifier TOK_DOT Id '''

      4,6,5,7
   if(len(p) == 4):
      p[0] = Node("stableId", [p[1], p[2], p[3]])
   else if(len(p) == 5):
      p[0] = Node("stableId", [p[1], p[2], p[3], p[4]])
   else if(len(p) == 6):
      p[0] = Node("stableId", [p[1], p[2], p[3], p[4], p[5]])
   else:
      p[0] = Node("stableId", [p[1], p[2], p[3], p[4], p[5], p[6]])
   
'''
classQualifier
   : '[' Id ']'
   ;
'''
def p_classQualifier(p):
   '''classQualifier  : TOK_LSQB Id TOK_RSQB '''

   p[0] = Node("classQualifier", [p[1], p[2], p[3]])

'''
type
   : functionArgTypes '=>' type
   | infixType existentialClause?
   ;
'''
def p_type(p):
   '''type  : functionArgTypes TOK_EQ_GT type  | infixType | infixType existentialClause  '''

   if(len(p) == 2):
      p[0] = Node("type", [p[1]])
   else if(len(p) == 3):
      p[0] = Node("type", [p[1], p[2]])
   else:
      p[0] = Node("type", [p[1], p[2], p[3]])

'''
functionArgTypes
   : infixType
   | '(' (paramType (',' paramType)*)? ')'
   ;
'''
def p_functionArgTypes(p):
   '''functionArgTypes : infixType   | TOK_LPAREN TOK_RPAREN 
                       | TOK_LPAREN paramType TOK_COMMA_paramTypes_opt TOK_RPAREN '''
   if(len(p) == 2):
      p[0] = Node("functionArgTypes", [p[1]])
   else if (len(p) == 3):
      p[0] = Node("functionArgTypes", [p[1], p[2]])
   else:
      p[0] = Node("functionArgTypes", [p[1], p[2], p[3], p[4]])

def p_TOK_COMMA_paramTypes_opt(p):
   '''TOK_COMMA_paramTypes_opt : TOK_COMMA_paramTypes | empty '''

   p[0] = Node("TOK_COMMA_paramTypes_opt", [p[1]])

def p_TOK_COMMA_paramTypes(p):
   '''TOK_COMMA_paramTypes : TOK_COMMA_paramType | TOK_COMMA_paramTypes TOK_COMMA_paramType '''

   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_paramTypes", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_paramTypes", [p[1], p[2]])

def p_TOK_COMMA_paramType(p):
   '''TOK_COMMA_paramType : TOK_COMMA paramType '''

   p[0] = Node("TOK_COMMA_paramType", [p[1], p[2]])

'''
existentialClause
   : 'forSome' '{' existentialDcl (Semi existentialDcl)* '}'
   ;
'''
def p_existentialClause(p):
   '''existentialClause  : TOK_forSome TOK_LCUR existentialDcl TOK_SEMICOLON_existentialDcls_opt TOK_RCUR  '''

   p[0] = Node("existentialClause", [p[1], p[2], p[3], p[4], p[5]])

def p_TOK_SEMICOLON_existentialDcls_opt(p):
   '''TOK_SEMICOLON_existentialDcls_opt : TOK_SEMICOLON_existentialDcls | empty '''

   p[0] = Node("TOK_SEMICOLON_existentialDcls_opt", [p[1]])

def p_TOK_SEMICOLON_existentialDcls(p):
   '''TOK_SEMICOLON_existentialDcls : TOK_SEMICOLON_existentialDcl | TOK_SEMICOLON_existentialDcls TOK_SEMICOLON_existentialDcl '''

   if(len(p) == 2):
      p[0] = Node("TOK_SEMICOLON_existentialDcls", [p[1]])
    else:
      p[0] = Node("TOK_SEMICOLON_existentialDcls", [p[1], p[2]])

def p_TOK_SEMICOLON_existentialDcl(p):
   '''TOK_SEMICOLON_existentialDcl : TOK_SEMICOLON existentialDcl '''

   p[0] = Node("TOK_SEMICOLON_existentialDcl", [p[1], p[2]])
   

'''
existentialDcl
   : 'type' typeDcl
   | 'val' valDcl
   ;
'''
def p_existentialDcl(p):
   '''existentialDcl  : TOK_type typeDcl  | TOK_val valDcl '''

   p[0] = Node("existentialDcl", [p[1], p[2]])

'''
infixType
   : compoundType (Id compoundType)*
   ;
'''
def p_infixType(p):
   '''infixType   : compoundType id_compoundTypes_opt '''
   p[0] = Node("infixType", [p[1], p[2]])

def p_id_compoundTypes_opt(p):
   '''id_compoundTypes_opt : id_compoundTypes | empty '''

   p[0] = Node("id_compoundTypes_opt", [p[1]])

def p_id_compoundTypes(p):
   '''id_compoundTypes : id_compoundType | id_compoundTypes id_compoundType '''

   if(len(p) == 2):
      p[0] = Node("id_compoundTypes", [p[1]])
    else:
      p[0] = Node("id_compoundTypes", [p[1], p[2]])


def p_id_compoundType(p):
   '''id_compoundType : id compoundType '''

   p[0] = Node("id_compoundType", [p[1], p[2]])

'''
compoundType
   : annotType ('with' annotType)* refinement?
   | refinement
   ;
'''

def p_compoundType(p):
   '''compoundType   : annotType TOK_with_annotTypes_opt | annotType TOK_with_annotTypes_opt refinement  | refinement '''
   if(len(p) == 3):
      p[0] = Node("compoundType", [p[1],p[2]])
   else if(len(p) == 4):
      p[0] = Node("compoundType", [p[1], p[2],p[3]])
   else : 
      p[0] = Node("compoundType", [p[1]])   	
def p_TOK_with_annotTypes_opt(p):
   ''' TOK_with_annotTypess_opt : TOK_with_annotTypes | empty '''
   p[0] = Node("TOK_with_annotTypess_opt", [p[1]])
def p_TOK_with_annotTypes(p):
   ''' TOK_with_annotTypes : TOK_with_annotType | TOK_with_annotTypes TOK_with_annotType '''
   if(len(p) == 2):
      p[0] = Node("TOK_with_annotTypes", [p[1]])
    else:
      p[0] = Node("TOK_with_annotTypes", [p[1], p[2]])

def p_TOK_with_annotType(p):
   ''' TOK_with_annotType : TOK_with annotType '''
   p[0] = Node("TOK_with_annotType", [p[1]])
'''
annotType
   : simpleType annotation*
   ;
'''
#annotations_opt defined beforehand
def p_annotType(p):
   '''annotType : simpleType annotations_opt '''
   p[0] = Node("annotType", [p[1],p[2]])

'''
simpleType
   : simpleType typeArgs
   | simpleType '#' Id
   | stableId
   | (stableId | (Id '.')? 'this') '.' 'type'
   | '(' types ')'
   ;
'''
#to do error
def p_simpleType(p):
	'''simpleType   : simpleType typeArgs   | simpleType TOK_HASH Id   | stableId | 
	TOK_this TOK_DOT TOK_type | Id TOK_DOT TOK_this TOK_DOT TOK_type  | stableId TOK_DOT TOK_type  | 
	TOK_LPAREN types TOK_RPAREN '''

'''
typeArgs
   : '[' types ']'
   ;
'''
def p_typeArgs(p):
   '''typeArgs  : TOK_LSQB types TOK_RSQB '''
   p[0] = Node("typeArgs", [p[1],p[2],p[3]])

'''
types
   : type (',' type)*
   ;
'''
def p_types(p):
   '''types  : type TOK_COMMA_types_opt '''
   p[0] = Node("typeArgs", [p[1],p[2]])



def p_TOK_COMMA_types_opt(p):
   ''' TOK_COMMA_types_opt : TOK_COMMA_types | empty '''
   p[0] = Node("TOK_COMMA_types_opt", [p[1]])

def p_TOK_COMMA_types(p):
   ''' TOK_COMMA_types : TOK_COMMA_type | TOK_COMMA_types TOK_COMMA_type '''
   if(len(p) == 2):
      p[0] = Node("TOK_COMMA_types", [p[1]])
    else:
      p[0] = Node("TOK_COMMA_types", [p[1], p[2]])
def p_TOK_COMMA_type(p):
   ''' TOK_COMMA_type : TOK_COMMA type '''
   p[0] = Node("TOK_COMMA_type", [p[1]])


'''
refinement
   : '{' refineStat (Semi refineStat)* '}'
   ;
'''

def p_refinement(p):
   ''' refinement   : TOK_LCUR refineStat TOK_SEMICOLON_refineStats_opt TOK_RCUR '''
   p[0] = Node("refinement", [p[1],p[2],p[3],p[4]])

def p_TOK_SEMICOLON_refineStats_opt(p):
   ''' TOK_SEMICOLON_refineStats_opt : TOK_SEMICOLON_refineStats | empty '''
   p[0] = Node("TOK_SEMICOLON_refineStats_opt", [p[1]])

def p_TOK_SEMICOLON_refineStats(p):
   ''' TOK_SEMICOLON_refineStats : TOK_SEMICOLON_refineStat | TOK_SEMICOLON_refineStats TOK_SEMICOLON_refineStat '''
   if(len(p) == 2):
      p[0] = Node("TOK_SEMICOLON_refineStats", [p[1]])
    else:
      p[0] = Node("TOK_SEMICOLON_refineStats", [p[1], p[2]])

def p_TOK_SEMICOLON_refineStat(p):
   ''' TOK_SEMICOLON_refineStat : TOK_SEMICOLON refineStat '''
   p[0] = Node("TOK_SEMICOLON_refineStat", [p[1], p[2]])

'''
refineStat
   : dcl
   | 'type' typeDef
   |
   ;
'''
def p_refineStat(p):
   '''refineStat   : dcl   | TOK_type typeDef   |  empty    '''
   if(len(p) == 2):
      p[0] = Node("refineStat", [p[1]])
    else:
      p[0] = Node("refineStat", [p[1], p[2]])

'''
typePat
   : type
   ;
'''
def p_typePat(p):
   ''' typePat : type  '''
   p[0] = Node("typePat", [p[1]])
   

'''
ascription
   : ':' infixType
   | ':' annotation +
   | ':' '_' '*'
   ;
'''
def p_ascription(p):
   '''ascription  : TOK_COLON infixType   | TOK_COLON annotations   | TOK_COLON TOK_UNDERSCORE TOK_STAR  '''
   if(len(p) == 4):
      p[0] = Node("ascription", [p[1],p[2],p[3]])
    else:
      p[0] = Node("ascription", [p[1], p[2]])

'''
expr
   : (bindings | 'implicit'? Id | '_') '=>' expr
   | expr1
   ;
'''
def p_expr(p):
   '''expr  : temp TOK_EQ_GT expr   | expr1 '''
   if(len(p) == 4):
      p[0] = Node("expr", [p[1],p[2],p[3]])
    else:
      p[0] = Node("expr", [p[1]])

def p_temp(p):
   ''' temp : bindings | TOK_implicit Id | Id | TOK_UNDERSCORE'''
   if(len(p) == 3):
      p[0] = Node("expr", [p[1],p[2]])
    else:
      p[0] = Node("expr", [p[1]])




LEAF_NODES = [	'IDENTIFIER',
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
