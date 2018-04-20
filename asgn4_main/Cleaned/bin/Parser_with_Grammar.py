#!/usr/bin/python

from Scope_SymTab import *
from secondpass import secondpass

class Node(object): 
   count = 1

   def __init__(self, name, children, code = [], type = "Unit", size = None, value = None, place = None):
      self.name = name #name of the node, non terminal
      self.children = children
      self.id=Node.count
      Node.count+=1
      self.type = type
      self.value = value
      self.code = code
      self.size = size
      self.place = place

def create_children(token_name , terminal_name, type="Unit"):
   leaf_t = Node(terminal_name,[], [], type)
   leaf_token = Node(token_name,[leaf_t], [], type)
   return leaf_token


def exceptionHandler(exception_type, exception, traceback):

    print ("%s: %s "% (exception_type.__name__, exception))


'''sys.stderr = open('errors.log', 'w')
sys.excepthook = exceptionHandler
Error_message = "Error in Program"'''

CurrentScope = SymTable()
GlobalScope = CurrentScope

count_temp = 0
count_label = 0
FinalResult = " "

def newlabel():
   global count_label
   label_id = "label" + str(count_label)
   count_label += 1
   return label_id


def newtemp(dataType= 'Unit'):
   global count_temp
   symbol_id = "t" + str(count_temp)
   count_temp += 1
   attr= {'Type' : dataType}
   global CurrentScope
   CurrentScope.add_symbol(symbol_id, attr)
   return symbol_id


'''def higher(type1, type2):
   if(type1 == 'Float'):
      return type1
   elif (type2 == 'Float'):
      return type2
   else:
      return type1'''

def filter_list(input):
   res = []
   for t in input:
      if type(t) == list:
         res.append(t[0])
      else:
         res.append(t)
   return res

'''PROGRAM '''

def p_compilation_unit(p):
   '''compilation_unit : class_and_obj_declarations'''
   
   p[0]  = Node("compilationUnit", [p[1]], p[1].code)
   print(p[0].code)
   res = filter_list(p[0].code)
   FinalResult = ('\n').join(res)
   secondpass(FinalResult)
'''DECLARATIONS'''

def p_class_and_obj_declarations(p):
   '''class_and_obj_declarations : class_and_obj_declaration 
      | class_and_obj_declarations class_and_obj_declaration'''

   if(len(p) == 2):
      p[0] = Node("class_and_obj_declarations", [p[1]], p[1].code)

   else:
      p[0] = Node("class_and_obj_declarations", [p[1], p[2]], p[1].code + p[2].code)

def p_class_and_obj_declaration(p):
   '''class_and_obj_declaration : singleton_object  '''

   p[0]  = Node("class_and_obj_declaration", [p[1]], p[1].code)

def p_singleton_object(p):
   '''singleton_object : object_declaration block'''

   p[0]  = Node("singleton_object", [p[1], p[2]], p[2].code)

def p_object_declaration(p):
   '''object_declaration : KW_obj TOK_identifier'''
   global CurrentScope
   #CHECKFORTHIS
   #CurrentScope.object_list.append(p[2])
   leaf1 = create_children("KW_obj", p[1])
   leaf2 = create_children("TOK_identifier", p[2])
   p[0]  = Node("object_declaration", [leaf1, leaf2])
#
#def p_class_declaration(p):
#   '''class_declaration : KW_class name class_body'''
#
#   leaf1 = create_children("KW_class", p[1])
#   p[0]  = Node("class_declaration", [leaf1, p[2], p[3]])

'''BLOCK DEFINITION'''

def p_block(p):
   '''block : TOK_lcurly block_stats_star TOK_rcurly'''

   leaf1 = create_children("TOK_lcurly", p[1])
   leaf3 = create_children("TOK_rcurly", p[3])
   p[0]  = Node("block", [leaf1, p[2], leaf3], p[2].code)

def p_block_stats_star(p):
   '''block_stats_star : block_stats 
   | empty '''

   p[0]  = Node("block_stats_star", [p[1]], p[1].code)   

def p_block_stats(p):
   '''block_stats : block_stat 
   | block_stats block_stat'''

   if(len(p) == 2):
      p[0] = Node("block_stats", [p[1]], p[1].code)

   else:
      p[0] = Node("block_stats", [p[1], p[2]], p[1].code + p[2].code)

def p_block_stat(p):
   '''block_stat : local_variable_declaration_statement 
            | statement 
            | class_and_obj_declaration 
            | method_declaration'''

   p[0] = Node("block_stat", [p[1]], p[1].code)

'''EXPRESSION'''

def p_expression_question(p):
   '''expression_question : expression 
   | empty '''


   p[0] = Node("expression_question", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place, value = p[1].value)

def p_expression(p):
   '''expression : assignment_expression '''


   p[0] = Node("expression", [p[1]], p[1].code, p[1].type, place = p[1].place )

def p_assignment_expression(p):
   '''assignment_expression : assignment 
                           | conditional_or_expression
                           | method_invocation'''


   p[0] = Node("assignment_expression", [p[1]], p[1].code, p[1].type, place = p[1].place)

'''def p_if_else_expression(p):
    if_else_expression : KW_if TOK_paraleft expression TOK_pararight expression KW_else expression 

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])
   leaf6 = create_children("KW_else", p[6])
   p[0] = Node("if_else_expression", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]])'''

#CHECKFORTHIS
def p_assignment(p):
   ''' assignment : left_hand_side assignment_operator assignment_expression '''

   if(p[1].type != p[3].type):
      raise Exception("Type Mismatch in Assignment in line", p.lexer.lineno)
   if(p[2].place == "="):
      tac = ['=,' + p[1].place  + ',' + p[3].place]
      p[0] = Node("assignment", [p[1],p[2],p[3]],  code = p[1].code + p[3].code + tac)
   else:
      if(p[1].place[-1] == ']'):
         temp = newtemp()
         tac1 = [p[2].place[:-1] + ',' + temp + ',' + temp + ',' + p[3].place]
         tac2 = ['=,' + p[1].place + ',' + temp]
         tac = tac1 + tac2
      else:
         tac = [p[2].place[:-1] + ','+ p[1].place + ',' + p[1].place + ',' + p[3].place]
   p[0] = Node("assignment", [p[1],p[2],p[3]], code = p[1].code + p[3].code + tac)


def p_left_hand_side1(p):
   ''' left_hand_side : id '''

   global CurrentScope
   (x, y) = CurrentScope.find_var_decl(p[1].place)
   if(x == 0):
      raise Exception("Undeclared Variable " + str(p[1]), p.lexer.lineno)
   else:
      #variable = str(y.id) + "_" + p[1].place
      variable = p[1].place
      type1 = y.symbols[p[1].place]['Type']
   p[0] = Node("left_hand_side", [p[1]],code = p[1].code, place = variable, type = type1, value = p[1].value , size = p[1].value )


def p_left_hand_side2(p):
   '''left_hand_side : array_access'''
   
   p[0] = Node("left_hand_side", [p[1]],code = p[1].code, place = p[1].place, type = p[1].type, value = p[1].value , size = p[1].value )

def p_id(p):
   ''' id : name 
   | qualified_id '''
   
   # No Code needed here. We only need to pass values place etc.
   p[0] = Node("id", [p[1]], code = [], type = p[1].type, size = p[1].size , value = p[1].value, place = p[1].place)

def p_qualified_id(p):
   '''qualified_id : name TOK_dot name '''
   
   leaf2 = create_children("TOK_dot", p[2])
   
   #NoT Implemented
   p[0] = Node("qualified_id", [p[1], leaf2, p[3]],type = p[3].type , size = p[3].size, value = p[1].value + '.' + p[3].value, code = [])

def p_name(p):
   '''name : TOK_identifier '''

   #global CurrentScope
   leaf1 = create_children("TOK_identifier", p[1])
   p[0] = Node("name", [leaf1], code = [] ,value = p[1] , type = p[1], place = p[1] )

def p_array_access(p):
   ''' array_access : id dimension '''

   
   (x, y) = CurrentScope.find_var_decl(p[1].place)
   if(x == 0):
      raise Exception("Undeclared Variable", p.lexer.lineno)
   else:
      temp_type = y.symbols[p[1].place]['Type'][:5]
      val_type  = y.symbols[p[1].place]['Type'][6:]
      if( temp_type != "Array"):
         raise Exception("Variable is not of type " + str(temp_type), p.lexer.lineno)

   #temp = newtemp(val_type)
   #tac1 = ["=," + temp + ','  + p[1].place + ' ' +  p[2].place]
   place1 = p[1].place + ' ' +  p[2].place   
   p[0]  = Node("array_access", [p[1], p[2]], code = p[2].code , type = val_type, place = place1)

def p_dimension(p):
   ''' dimension : TOK_lsqb expression TOK_rsqb '''


   leaf1 = create_children("TOK_lsqb", p[1])
   leaf3 = create_children("TOK_rsqb", p[3])
   if(p[2].type != 'Int'):
      raise Exception("Acces Element should be an integer " + str(p[1].place), p.lexer.lineno)

   p[0] = Node("dimension", [leaf1,p[2],leaf3], place = '[ ' + p[2].place + ' ]' , code = p[2].code )

   '''else:
               leaf2 = create_children("TOK_lsqb", p[2])
               leaf4 = create_children("TOK_rsqb", p[4])
               p[0] = Node("class_and_obj_declarations", [p[1], leaf2, p[3], leaf4])'''

#| <<= | >>= | >>>= | &= | ^= | |= 
def p_assignment_operator(p):
   ''' assignment_operator : TOK_assignment 
   | TOK_mulassign 
   | TOK_divassign 
   | TOK_modassign 
   | TOK_addassign 
   | TOK_subassign '''


   leaf1 = create_children("LF_AssignOp", p[1])
   p[0] = Node("assignment_operator", [leaf1], place = p[1])

def p_conditional_or_expression(p):
   ''' conditional_or_expression : conditional_and_expression 
   | conditional_or_expression TOK_or conditional_and_expression '''

   if(len(p) == 2):
      p[0] = Node("conditional_or_expression", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place)

   else:
      leaf2 = create_children("TOK_or", p[2])
      temp = newtemp(p[1].type)
      tac1 = ["||," + temp + ',' + p[1].place + ',' + p[3].place]
      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      else:
         p[0] = Node("conditional_or_expression", [p[1], leaf2, p[3]], code = p[1].code + p[3].code + tac1, type = p[1].type, place = temp)


def p_conditional_and_expression(p):
      '''conditional_and_expression : inclusive_or_expression
                             | conditional_and_expression TOK_and inclusive_or_expression'''
      if len(p) == 2:
         p[0] = Node("conditional_and_expression", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place)
      else:
         leaf1 = create_children("TOK_and", p[2])
         if(p[1].type != p[3].type):
            raise Exception("Type mismatch in line ", p.lexer.lineno)

         temp = newtemp(p[1].type)
         tac1 = ['&&,' + temp + ',' + p[1].place + ',' + p[3].place]
         p[0] = Node("conditional_and_expression", [p[1], leaf1, p[3]] , code = p[1].code + p[3].code + tac1, place = temp, type = p[1].type)

def p_inclusive_or_expression(p):
   '''inclusive_or_expression : exclusive_or_expression  
   | inclusive_or_expression TOK_or_bitwise exclusive_or_expression'''
  

   if(len(p) == 2):
      p[0] = Node("inclusive_or_expression", [p[1]], code = p[1].code , place = p[1].place , type = p[1].type)

   else:
      leaf2 = create_children("TOK_or_bitwise", p[2])
      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = ['| ,' + temp + ',' + p[1].place + ',' + p[3].place]
      p[0] = Node("inclusive_or_expression", [p[1], leaf2, p[3]], place = temp , type = p[1].type , code = p[1].code + p[3].code + tac1)

def p_exclusive_or_expression(p):
   ''' exclusive_or_expression : and_expression 
                                 | exclusive_or_expression TOK_xor and_expression '''

   if(len(p) == 2):
      p[0] = Node("exclusive_or_expression", [p[1]] , type = p[1].type, code = p[1].code , place = p[1].place)

   else:
      leaf2 = create_children("TOK_xor", p[2])
      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = ['^ ,' + temp + ',' + p[1].place + ',' + p[3].place]

      p[0] = Node("exclusive_or_expression", [p[1], leaf2, p[3]], place = temp , type = p[1].type , code = p[1].code + p[3].code + tac1)

def p_and_expression(p):
   ''' and_expression : equality_expression 
   | and_expression TOK_and_bitwise equality_expression '''

   if(len(p) == 2):
      p[0] = Node("and_expression", [p[1]] , type = p[1].type , place = p[1].place , code = p[1].code )

   else:
      leaf2 = create_children("TOK_and_bitwise", p[2])
      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = ['& ,' + temp + ',' + p[1].place + ',' + p[3].place]
      p[0] = Node("and_expression", [p[1], leaf2, p[3]], place = temp , type = p[1].type , code = p[1].code + p[3].code + tac1)


def p_equality_expression(p):
   '''equality_expression : relational_expression
                        | equality_expression TOK_equal relational_expression
                        | equality_expression TOK_nequal relational_expression'''


   if(len(p) == 2):
      p[0] = Node("equality_expression", [p[1]], code = p[1].code , type = p[1].type , place = p[1].place)

   else:
      leaf2 = create_children("LF_EqualityOp", p[2])

      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)

      temp = newtemp(p[1].type)
      tac1 = ["=,"+ temp + ',' + '0']
      tac2 = [ p[2] + ' ,' + temp + ',' + p[1].place + ',' + p[3].place]

      p[0] = Node("equality_expression", [p[1], leaf2, p[3]], place = temp , type = p[1].type , code = p[1].code + p[3].code + tac1 + tac2)


def p_relational_expression(p):
   '''relational_expression : shift_expression
                         | relational_expression TOK_greater shift_expression
                         | relational_expression TOK_lesser shift_expression
                         | relational_expression TOK_geq shift_expression
                         | relational_expression TOK_leq shift_expression'''

   if(len(p) == 2):
      p[0] = Node("relational_expression", [p[1]] , code=p[1].code, type=p[1].type, place=p[1].place)

   else:
      leaf2 = create_children("LF_RelationalOp", p[2])

      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = ["=,"+ temp + ',' + '0']
      tac2 = [p[2] + ',' + temp + ',' + p[1].place + ',' + p[3].place]

      p[0] = Node("relational_expression", [p[1], leaf2, p[3]], place = temp , type = p[1].type , code = p[1].code + p[3].code + tac1 + tac2)


def p_shift_expression(p):
   '''shift_expression : additive_expression
                           | shift_expression TOK_lshift additive_expression
                           | shift_expression TOK_rshift additive_expression'''

   if(len(p) == 2):
      p[0] = Node("shift_expression", [p[1]], place = p[1].place, code = p[1].code, type=p[1].type)

   else:
      leaf2 = create_children("LF_ShiftOp", p[2])

      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = [p[2] + ' ,' + temp + ',' + p[1].place + ',' + p[3].place]


      p[0] = Node("shift_expression", [p[1], leaf2, p[3]], place = temp, code = p[1].code + p[3].code + tac1, type = p[1].type )

def p_additive_expression(p):
   '''additive_expression : multiplicative_expression
                         | additive_expression TOK_plus multiplicative_expression
                         | additive_expression TOK_minus multiplicative_expression'''

   if(len(p) == 2):
      p[0] = Node("additive_expression", [p[1]] , place = p[1].place , code = p[1].code , type = p[1].type)

   else:
      leaf2 = create_children("LF_AdditiveOp", p[2])

      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = [p[2] + ' ,' + temp + ',' + p[1].place + ',' + p[3].place]

      p[0] = Node("additive_expression", [p[1], leaf2, p[3]], place = temp, code = p[1].code + p[3].code + tac1, type = p[1].type)

def p_multiplicative_expression(p):
   '''multiplicative_expression : unary_expression
                            | multiplicative_expression TOK_times unary_expression
                            | multiplicative_expression TOK_divide unary_expression
                            | multiplicative_expression TOK_modulus unary_expression'''

   if(len(p) == 2):
      p[0] = Node("multiplicative_expression", [p[1]], place = p[1].place, type = p[1].type , code = p[1].code )

   else:
      leaf2 = create_children("LF_MultiplicativeOp", p[2])

      if(p[1].type != p[3].type):
         raise Exception("Type mismatch in line ", p.lexer.lineno)
      temp = newtemp(p[1].type)
      tac1 = [p[2] + ' ,' + temp + ',' + p[1].place + ',' + p[3].place]

      p[0] = Node("multiplicative_expression", [p[1], leaf2, p[3]], code = p[1].code + p[3].code + tac1 , place = temp, type = p[1].type)


def p_unary_expression(p):
   '''unary_expression : TOK_plus unary_expression
                     | TOK_minus unary_expression
                     | unary_expression_not_plus_minus'''

   if(len(p) == 2):
      p[0] = Node("unary_expression", [p[1]] , code = p[1].code , place = p[1].place , type = p[1].type)

   else:
      leaf1 = create_children("LF_Unaryop", p[1])

      temp = newtemp(p[2].type)
      tac1 = [p[1] + ' ,' + temp + ',' + p[1].place ]

      p[0] = Node("unary_expression", [leaf1, p[2]], code = p[2].code + tac1, place = temp , type = p[2].type )

#if possible implement | TOK_tilda unary_expression | cast_expression
def p_unary_expression_not_plus_minus(p):
   '''unary_expression_not_plus_minus : base_variable_set                  
                                  | TOK_not unary_expression''' 
   
   if(len(p) == 2):
      p[0] = Node("unary_expression_not_plus_minus", [p[1]] , place = p[1].place , code = p[1].code , type = p[1].type , value = p[1].value)

   else:
      leaf1 = create_children("LF_Unarydiffop", p[1])
      temp = newtemp(p[2].type)
      tac1 = ['!' + ',' + temp + ',' + p[2].place ]
      p[0] = Node("unary_expression_not_plus_minus", [leaf1, p[2]], type = p[2].type, code = p[2].code + tac1 , place = temp)

def p_base_variable_set(p):
   '''base_variable_set : variable_literal
                   | TOK_paraleft expression TOK_pararight'''

   if(len(p) == 2):
      p[0] = Node("base_variable_set", [p[1]], place=p[1].place , code = p[1].code , value = p[1].value, type = p[1].type )

   else:
      leaf1 = create_children("TOK_paraleft", p[1])
      leaf3 = create_children("TOK_pararight", p[3])
      p[0] = Node("base_variable_set", [leaf1, p[2], leaf3] , code = p[2].code , place = p[2].place , type = p[2].type)


def p_variable_literal(p):
   '''variable_literal : left_hand_side 
   | primary'''

   p[0] = Node("variable_literal", [p[1]], code = p[1].code , place = p[1].place , type = p[1].type , value = p[1].value )

'''
def p_cast_expression(p):
   cast_expression : TOK_paraleft primitive_type TOK_pararight unary_expression

   leaf1 = create_children("TOK_paraleft", p[1])
   leaf3 = create_children("TOK_pararight", p[3])

   p[0] = Node("cast_expression", [leaf1, p[2], leaf3, p[4]])
'''

def p_primary(p):
   '''primary : literal 
               | method_invocation'''
   
      
   p[0] = Node("primary", [p[1]] , code = p[1].code, place = p[1].place, type = p[1].type, value = p[1].value)


def p_literal(p):
   '''literal : int_float  
   | c_literal ''' 

   p[0] = Node("literal", [p[1]], code = p[1].code, place = p[1].place, type = p[1].type, value = p[1].value)

#CHECKFORTHIS
def p_c_literal1(p):
   '''c_literal : TOK_string
               | KW_true
               | KW_false
               | KW_null '''


   leaf1 = create_children("LF_Charliteral", p[1])
   if(p[1] == 'True' or p[1] == 'False'):
      temp_type = 'Boolean'
      temp = newtemp()
      tac1 = ['=,' + temp + ',' + p[1]]
   elif(p[1] == 'null'):
      temp_type = 'Unit'
      temp = newtemp()
      tac1 = ['=,' + temp + ',' + p[1]]
   else:
      temp_type = 'String'
      temp = newtemp(temp_type)
      stringexp = '"' + p[1] + '"'
      tac1 = ['=s,' +  temp + ',' +  stringexp ]
   p[0] = Node("c_literal", [leaf1] , code = tac1, place = temp , type = temp_type, value = p[1])


def p_c_literal2(p):
   '''c_literal : TOK_char '''

   leaf1 = create_children("LF_Charliteral", p[1])
   temp = newtemp('Char')
   tac1 = ['=,' +  temp + ',' + str(p[1]) ]

   p[0] = Node("c_literal", [leaf1] , code = tac1, place = temp , type = 'Char', value = p[1])


#CHECKFORTHIS
def p_int_float1(p):
   '''int_float : TOK_float '''

   leaf1 = create_children("LF_IntFloat", p[1])

   temp = newtemp('Float')
   tac1 = ['=,' +  temp + ',' + str(p[1]) ]

   p[0] = Node("int_float", [leaf1] , code = tac1, place = temp, type = 'Float' , value = p[1] )

def p_int_float2(p):
   '''int_float : TOK_int '''

   leaf1 = create_children("LF_IntFloat", p[1])

   temp = newtemp('Int')
   tac1 = ['=,' +  temp + ',' + str(p[1]) ]

   p[0] = Node("int_float", [leaf1] , code = tac1, place = temp, type = 'Int' , value = p[1] )

#FUNCTION CALLS

def p_method_invocation(p):
   '''method_invocation : id TOK_paraleft argument_list_question TOK_pararight '''
   
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])
   code1 = []


   if(p[1].value == "println"):
      for i in range(0, len(p[3].type)):
         if(p[3].type[i] == 'Int'):
            #function_name = "println"
            #temp = newtemp()
            #code1.append("=," + temp + ',' + p[3].place[i])
            code1.append("print," + p[3].place[i])
         elif(p[3].type[i] == 'String'):
            #function_name = "println"
            #code1.append("=s," + temp + ',' + p[3].place[i])
            code1.append("print," + p[3].place[i])
      code1.append("print,newline")
      p[0] = Node("method_invocation", [p[1], leaf2, p[3], leaf4], code = p[1].code + p[3].code + code1, place = None, type = "Unit")
      return

   if(p[1].value == "read"):
      if (len(p[3].type) > 1):
         raise Exception("read only takes one argument", p.lexer.lineno)
      temp = newtemp()
      code1.append("=,"+ temp + ',' + '0')
      code1.append("scan," + temp)
      code1.append("=," + p[3].place[0] + ',' + temp)
      p[0] = Node("method_invocation", [p[1], leaf2, p[3], leaf4], code = p[1].code + p[3].code + code1, place = None, type = "Unit")
      return

   global CurrentScope
   retval = None
   (x, y) = CurrentScope.find_func_decl(p[1].place)
   if(x == 0):
      raise Exception("Function not Declared", p.lexer.lineno)
   elif (p[3].value != y.functions[p[1].place]["num_args"]):
      raise Exception("Number of arguments do not match", p.lexer.lineno)
   else:
      #function_name = str(y.id) + '_' + p[1].place
      function_name = p[1].place


   
   for i in p[3].place:
      code1.append(['param,'  + str(i)])

   code1.append(['call,' + function_name])
   return_type = y.functions[p[1].place]['ReturnType'] 
   if(return_type != 'Unit'):
      retval = newtemp(return_type)
      code1.append(['ret,' + retval])

   p[0] = Node("method_invocation", [p[1], leaf2, p[3], leaf4], code = p[1].code + p[3].code + code1, place = retval, type = return_type)


def p_argument_list_question(p):
   ''' argument_list_question : argument_list 
   | empty'''

   if(p[1].value == None):
      p[1].value = 0
   if(p[1].place == None):
      p[1].place = []                      
   p[0] = Node("argument_list_question", [p[1]], code = p[1].code, place = p[1].place, type = p[1].type, value = p[1].value)


def p_argument_list(p):
   '''argument_list : expression
                  | argument_list TOK_comma expression'''
   
   if(len(p) == 2):
      p[0] = Node("argument_list", [p[1]], code = p[1].code, place = [p[1].place], type = [p[1].type], value = 1)

   else:
      leaf2 = create_children("TOK_comma", p[2])
      p[0] = Node("argument_list", [p[1], leaf2, p[3]], code = p[1].code + p[3].code, place = p[1].place + [p[3].place], type = p[1].type + [p[3].type], value = 1 + p[1].value)
      #Value denotes the number of arguments
                     

'''LOCAL VARIABLE DECLARATION'''


def p_declaration_keyword(p):
   '''declaration_keyword : KW_var 
   | KW_val '''

   leaf1 = create_children("LF_Declaration", p[1])
   p[0] = Node("declaration_keyword", [leaf1], place = p[1], value = p[1])


def p_local_variable_declaration_statement(p):
   '''local_variable_declaration_statement : local_variable_declaration TOK_semi '''
   leaf2 = create_children("TOK_semi", p[2])
   p[0] = Node("local_variable_declaration_statement", [p[1],leaf2], type = p[1].type , code = p[1].code)


def p_local_variable_declaration(p):
   '''local_variable_declaration : declaration_keyword variable_declaration_body'''

   p[0] = Node("local_variable_declaration", [p[1],p[2]], code = p[2].code, type = p[2].type)


def p_variable_declaration_initializer(p):
   '''variable_declaration_initializer : expression
                              | array_initializer'''

   p[0] = Node("variable_declaration_initializer", [p[1]], place = p[1].place , type = p[1].type, code = p[1].code, value = p[1].value)

def p_variable_declaration_body(p):
   '''variable_declaration_body : TOK_identifier type_question TOK_assignment  variable_declaration_initializer '''

   
   leaf1 = create_children("TOK_identifier", p[1])
   leaf3 = create_children("TOK_assignment", p[3])
   global CurrentScope
   if (p[1] in CurrentScope.symbols.keys()):
      raise Exception("Variable already defined " + str[p[1]], p.lexer.lineno)
   elif(p[2].type != p[4].type):
      raise Exception("Type mismatch in line", p.lexer.lineno)
   else:
      attr = {}
      attr['Type'] = p[2].type
      attr['Size'] = p[2].size
      CurrentScope.add_symbol(p[1], attr)
      #variable = str(CurrentScope.id) + '_' + p[1]
      variable = p[1]
      if(p[4].value == "Array"):
         cd = p[4].place[0] + p[1] + p[4].place[1]
         tac1 = [cd]
      else:
         tac1 = ['=,' + variable + ',' + p[4].place]
      p[0] = Node("variable_declaration_body", [leaf1, p[2], leaf3, p[4]], code = p[4].code + tac1, place = variable, type = p[2].type)


def p_variable_declarator_id(p):
   '''variable_declarator_id : TOK_identifier TOK_colon type'''

   global CurrentScope
   if(p[1] in CurrentScope.symbols.keys()):
      raise Exception("Variable already defined " + str(p[1]), p.lexer.lineno)

   else:
      attr = {}
      attr['Type'] = p[3].type
      attr['Size'] = p[3].size
      CurrentScope.add_symbol(p[1], attr)
      #variable = str(CurrentScope.id) + "_" + p[1]
      variable = p[1]
      leaf1 = create_children("TOK_identifier", p[1])
      leaf2 = create_children("TOK_colon", p[2])
      p[0] = Node("variable_declarator_id", [leaf1, leaf2, p[3]], code = [], type = p[3].type, place = variable, value = 1)


#DATA_TYPES AND VARIABLE_TYPES

#theirs - ours
#Simple Name - name
#Name - id
#qualified name: qualified_id

def p_type(p):
   '''type : primitive_type 
   | reference_type '''

   p[0] = Node("type", [p[1]], value = p[1].value, place = p[1].place , type = p[1].type )

#CHECKFORTHIS
def p_primitive_type(p):
   '''primitive_type : KW_int
                  | KW_double
                  | KW_char
                  | KW_string
                  | KW_boolean 
                  | KW_void   '''


   leaf1 = create_children("LF_Primitivetype", p[1])
   p[0] = Node("primitive_type", [leaf1] , value = p[1], place = p[1], type = p[1])


def p_reference_type(p):
   '''reference_type : array_data_type'''

   p[0] = Node("reference_type", [p[1]], type = p[1].type, place = p[1].place, value = p[1].value)


def p_array_data_type(p):
   '''array_data_type : KW_array TOK_lsqb type TOK_rsqb'''

   
   leaf1 = create_children("KW_array", p[1])
   leaf2 = create_children("TOK_lsqb", p[2])
   leaf4 = create_children("TOK_rsqb", p[4])
   p[0] = Node("array_data_type", [leaf1, leaf2, p[3], leaf4], type = 'Array_' + p[3].type)

# INITIALIZERS

def p_array_initializer(p):
   ''' array_initializer : KW_new KW_array TOK_lsqb type TOK_rsqb TOK_paraleft TOK_int TOK_pararight'''



   leaf1 = create_children("KW_new", p[1])
   leaf2 = create_children("KW_array", p[2])
   leaf3 = create_children("TOK_lsqb", p[3])
   leaf5 = create_children("TOK_rsqb", p[5])
   leaf6 = create_children("TOK_paraleft", p[6])
   leaf7 = create_children("TOK_int", p[7])
   leaf8 = create_children("TOK_pararight", p[8])
   type1 = 'Array_' + str(p[4].type)
   #temp = newtemp()
   size1 = 4 * int(p[7])
   tac1 = ['Array,', ',' + str(size1) + str(p[7])] 
   p[0] = Node("array_initializer", [leaf1, leaf2, leaf3, p[4], leaf5, leaf6, leaf7, leaf8], code = [], type = type1, place = tac1, value = 'Array')


#Statements
def p_statement(p):
   '''statement : normal_statement 
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement'''
   
   p[0] = Node("statement", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place)

def p_normal_statement(p):
   '''normal_statement : block 
                  | expression_statement
                  | empty_statement
                  | return_statement'''

   p[0] = Node("normal_statement", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place)

def p_expression_statement(p):
   '''expression_statement : statement_expression TOK_semi'''

   leaf2 = create_children("TOK_semi", p[2])
   p[0] = Node("expression_statement", [p[1], leaf2], code = p[1].code, type = p[1].type, place = p[1].place)


def p_statement_expression(p):
   '''statement_expression : assignment
                           | method_invocation '''
   
   p[0] = Node("statement_expression", [p[1]], code = p[1].code, type = p[1].type, place = p[1].place)


#IF THEN STATEMENT
def p_if_then_statement(p):
   '''if_then_statement : KW_if TOK_paraleft expression TOK_pararight statement'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])   
   elselabel = newlabel()
   temp_code = p[3].code[-1]
   temp_list = temp_code.split(',')
   if(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '<'):
      temp_list[0] = '>='
   elif(temp_list[0] == '>='):
      temp_list[0] = '<'
   elif(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '=='):
      temp_list[0] = '!='
   elif(temp_list[0] == '!='):
      temp_list[0] = '=='
   tac1 = ["ifgoto," + elselabel + ',' + str(temp_list[0]) + ',' + str(temp_list[2]) + ',' + str(temp_list[3])]
   tac2 = ["label," + elselabel]
   p[0] = Node("if_then_statement", [leaf1, leaf2, p[3], leaf4, p[5]], code = p[3].code[:-1] + tac1 + p[5].code + tac2)

def p_if_then_else_statement(p):
   '''if_then_else_statement : KW_if TOK_paraleft expression TOK_pararight if_then_else_intermediate KW_else statement'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])
   leaf6 = create_children("KW_else", p[6])
   elselabel = newlabel()
   nextlabel = newlabel()
   temp_code = p[3].code[-1]
   temp_list = temp_code.split(',')
   if(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '<'):
      temp_list[0] = '>='
   elif(temp_list[0] == '>='):
      temp_list[0] = '<'
   elif(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '=='):
      temp_list[0] = '!='
   elif(temp_list[0] == '!='):
      temp_list[0] = '=='
   tac1 = ["ifgoto," + elselabel + ',' + str(temp_list[0]) + ',' + str(temp_list[2]) + ',' + str(temp_list[3]) ]
   tac2 = ["goto," + nextlabel]
   tac3 = ["label," + elselabel]
   tac4 = ["label," + nextlabel]
   p[0] = Node("if_then_else_statement", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]], code = p[3].code[:-1] + tac1 + p[5].code + tac2 + tac3 + p[7].code + tac4)


def p_if_then_else_statement_precedence(p):
   '''if_then_else_statement_precedence : KW_if TOK_paraleft expression TOK_pararight if_then_else_intermediate KW_else if_then_else_intermediate'''

   leaf1 = create_children("KW_if", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])
   leaf6 = create_children("KW_else", p[6])
   elselabel = newlabel()
   nextlabel = newlabel()
   if(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '<'):
      temp_list[0] = '>='
   elif(temp_list[0] == '>='):
      temp_list[0] = '<'
   elif(temp_list[0] == '<='):
      temp_list[0] = '>'
   elif(temp_list[0] == '=='):
      temp_list[0] = '!='
   elif(temp_list[0] == '!='):
      temp_list[0] = '=='
   tac1 = ["ifgoto," + elselabel + ',' + str(temp_list[0]) + ',' + str(temp_list[2]) + ',' + str(temp_list[3]) ]
   tac2 = ["goto," + nextlabel]
   tac3 = ["label," + elselabel]
   tac4 = ["label," + nextlabel]
   p[0] = Node("if_then_else_statement_precedence", [leaf1, leaf2, p[3], leaf4, p[5], leaf6, p[7]], code = p[3].code[:-1] + tac1 + p[5].code + tac2 + tac3 + p[7].code + tac4)


def p_if_then_else_intermediate(p):
   '''if_then_else_intermediate : normal_statement
                                     | if_then_else_statement_precedence'''

   p[0] = Node("if_then_else_intermediate", [p[1]], code = p[1].code)

def p_while_statement(p):
   '''while_statement : KW_while TOK_paraleft expression TOK_pararight statement'''

   leaf1 = create_children("KW_while", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])   
   leaf4 = create_children("TOK_pararight", p[4])
   beginlabel = newlabel()
   middlelabel = newlabel()
   nextlabel = newlabel()
   temp_code = p[3].code[-1]
   temp_list = temp_code.split(',')
   tac1 = ["label," + beginlabel]
   tac2 = ["ifgoto," + middlelabel + ',' +  str(temp_list[0]) + ',' + str(temp_list[2]) + ',' +  str(temp_list[3])]
   tac3 = ["label," + middlelabel]
   tac4 = ["goto," + nextlabel]
   tac5 = ["label," + nextlabel]
   tac6 = ["goto," + beginlabel]
   p[0] = Node("while_statement", [leaf1, leaf2, p[3], leaf4, p[5]], code = p[3].code[:-1] + tac1 + tac2 + tac4 + tac3 + p[5].code + tac6 + tac5)

# FOR_LOOP
#Implement Do While too

def p_for_statement(p):
   '''for_statement : KW_for TOK_paraleft for_update TOK_pararight statement '''
   
   leaf1 = create_children("KW_for", p[1])
   leaf2 = create_children("TOK_paraleft", p[2])
   leaf4 = create_children("TOK_pararight", p[4])
   beginlabel = newlabel()
   nextlabel = newlabel()
   iterator = p[1].value
   expr1 = p[3].place[1]
   expr2 = p[3].place[2]
   relop = p[3].place[0]
   update = p[3].place[3]
   tac1 = ["=," + iterator + ',' + expr1]
   tac2 = ["label," + beginlabel]
   tac3 = ["ifgoto," + nextlabel + ',' + relop + ',' + iterator + ',' + expr2]
   tac4 = ["+," + iterator + ',' + iterator + ',' + update]
   tac5 = ["goto," + beginlabel]
   tac6 = ["label," + nextlabel]
   p[0] = Node("for_statement", [leaf1, leaf2, p[3], leaf4, p[5]], code = p[3].code + tac1 + tac2 + tac3 + p[5].code + tac4 + tac5 + tac6)


def p_for_update(p):
   ''' for_update : for_loop for_step_opts '''

   place1 = p[1].place
   place1.append(p[2].place) #iterator update value
   p[0] = Node("for_update", [p[1], p[2],p[3]], place = place1, code = p[1].code, value = p[1].value)

#CHECKFORTHIS
def p_for_loop(p):
   ''' for_loop : TOK_identifier TOK_choose expression for_untilTo expression '''
   place1 = []
   place1.append(p[4].place)
   place1.append(p[3].place)
   place1.append(p[5].place)
   leaf1 = create_children("TOK_identifier", p[1])
   leaf2 = create_children("TOK_choose", p[2])
   #Iterator in value, loop condition in place
   p[0] = Node("for_loop", [leaf1, leaf2, p[3], p[4], p[5]], value = p[1], place = place1 , code = p[3].code + p[5].code)


def p_for_untilTo(p):
   '''for_untilTo : KW_until 
   | KW_to'''

   if(p[1] == 'until'):
      temp_string = '>='
   else:
      temp_string = '>'

   leaf1 = create_children("LF_Untito", p[1])
   p[0] = Node("for_untilTo", [p[1]], place = temp_string )

def p_for_step_opts(p):
   ''' for_step_opts : KW_by expression 
   | empty'''

   if len(p)==2:
      p[0]=Node("for_step_opts",[p[1]], place = 1)

   else :
      leaf1 = create_children("KW_by", p[1])
      p[0]=Node("for_step_opts",[leaf1, p[2]], place = p[2].place, code = p[2].code )

def p_empty_statement(p):
   '''empty_statement : TOK_semi '''
   leaf1 = create_children("TOK_semi", p[1])
   p[0] = Node("empty_statement", [leaf1])

def p_return_statement(p):
   '''return_statement : KW_return expression_question TOK_semi '''

   leaf3 = create_children("TOK_semi", p[3])
   leaf1 = create_children("KW_return", p[1])

   if(p[2].place == None and p[2].value == None):
      temp_code = ['ret']
   else:
      temp_code = ['ret ,' + p[2].place]

   p[0] = Node("return_statement", [leaf1, p[2], leaf3], code = p[2].code + temp_code , place = None)

def p_type_question(p):
   '''type_question : TOK_colon type '''

   leaf1 = create_children("TOK_colon",p[1])
   p[0] = Node("type_question",[leaf1, p[2]] , value = p[2].value, place = p[2].place, type = p[2].type)

# Method Declaration


#Implement Scoping here
def p_method_declaration(p):
   '''method_declaration : method_header method_body'''

   p[0] = Node("method_declaration", [p[1],p[2]], p[1].code + p[2].code)


#Implement Scoping here
def p_method_header1(p):
   '''method_header : KW_def name TOK_paraleft fun_params_question TOK_pararight type_question TOK_assignment'''

   global CurrentScope
   fun_attr = {}
   #fun_name = str(CurrentScope.id) + "_" + p[2].place
   fun_name = p[2].place
   tac1 = ["label," + fun_name]
   
   fun_attr['InputType'] = p[4].type #InputType
   fun_attr['num_args'] = p[4].value  
   fun_attr['ReturnType'] = p[6].type
   
   CurrentScope.add_function(p[2].place , fun_attr)
 
   leaf1 = create_children("KW_def", p[1])
   leaf3 = create_children("TOK_paraleft", p[3])
   leaf5 = create_children("TOK_pararight", p[5])
   leaf7 = create_children("TOK_assignment", p[7])
   p[0] = Node("method_header", [leaf1,p[2],leaf3,p[4],leaf5,p[6], leaf7], code = tac1 + p[4].code ,type = p[6].type)


def p_method_header2(p):
   '''method_header : KW_def name TOK_paraleft fun_params_question TOK_pararight '''

   global CurrentScope
   fun_attr = {}
   #fun_name = str(CurrentScope.id) + "_" + p[2].place
   fun_name = p[2].place
   tac1 = ["label," + fun_name]
   
   fun_attr['InputType'] = p[4].type #InputType
   fun_attr['num_args'] = p[4].value  
   fun_attr['ReturnType'] = 'Unit'
   
   CurrentScope.add_function(p[2].place , fun_attr)
 

   leaf1 = create_children("KW_def", p[1])
   leaf3 = create_children("TOK_paraleft", p[3])
   leaf5 = create_children("TOK_pararight", p[5])
   
   p[0] = Node("method_header", [leaf1,p[2],leaf3,p[4],leaf5], code = tac1 + p[4].code ,type = 'Unit')


def p_fun_params_question(p):
   '''fun_params_question : fun_params 
   | empty'''

   if(p[1].value == None and p[1].place == None):
      p[1].value = 0
      p[1].place = []
      p[1].type = 'Unit'

   p[0] = Node("fun_params_question", [p[1]], value = p[1].value, place = p[1].place, code = p[1].code, type = p[1].type )


def p_fun_params(p):
   '''fun_params : fun_param 
   | fun_params TOK_comma fun_param'''

   if(len(p) == 2):
      p[0] = Node("fun_params", [p[1]], place = [p[1].place], type = [p[1].type], code = p[1].code, value = p[1].value)

   else:
      leaf2 = create_children("TOK_comma", p[2])
      p[0] = Node("fun_params", [p[1], leaf2, p[3]], place = p[1].place + [p[3].place], type = p[1].type + [p[3].type], code = p[1].code + p[3].code, value = p[1].value + p[3].value )

def p_fun_param(p):
   '''fun_param : variable_declarator_id'''

   p[0] = Node("fun_param", [p[1]], type = p[1].type, place = p[1].place, value = p[1].value, code = p[1].code )

def p_method_body(p):
   '''method_body : block ''' 


   p[0] = Node("method_body", [p[1]], code = p[1].code)


#EMPTY DEFINITION

def p_empty(p):
   '''empty :'''
   leaf1 = create_children("", "")
   p[0] = Node("empty", [leaf1], value = None, place = None, code = [])



LEAF_NODES = ['KW_obj',
   'TOK_lcurly',
   'TOK_rcurly',
   'KW_if',
   'TOK_paraleft',
   'TOK_pararight',
   'KW_else',
   'TOK_identifier',
   'TOK_lsqb',
   'TOK_rsqb',
   'LF_AssignOp',
   'TOK_or',
   'TOK_or_bitwise',
   'TOK_xor',
   'TOK_and_bitwise',
   'LF_EqualityOp',
   'LF_RelationalOp',
   'LF_ShiftOp',
   'LF_AdditiveOp',
   'LF_MultiplicativeOp',
   'LF_Unaryop',
   'LF_Unarydiffop',
   'LF_Charliteral',
   'LF_Intliteral',
   'TOK_comma',
   'LF_Modifier',
   'LF_Declaration',
   'TOK_semi',
   'TOK_assignment',
   'TOK_colon',
   'LF_Primitivetype',
   'KW_array',
   'KW_new',
   'TOK_dot',
   'KW_ofdim',
   'KW_while',
   'KW_for',
   'TOK_choose',
   'LF_Untito',
   'KW_by',
   'KW_return',
   'KW_class',
   'KW_override',
   'KW_extends',
   'KW_def'
   ]

