class Node(object): 
	count = 1

	def __init__(self,name,children):
		self.name = name #name of the node, non terminal
		self.children = children
		self.id=Node.gid
		Node.gid+=1


def create_children(token_name , terminal_name):
	leaf_t = Node(terminal_name,[])
	leaf_token = Node(token_name,[leaf_t])
	return leaf_token






##############################



#Format: Rule in ANTLR form, followed by set of rules for yacc


#Note: for '*' or 0 or more we have _opt rule , for '+' one or more we have 's' rule
'''
compilationUnit
   : ('package' qualId Semi)* topStatSeq
   ;

'''
def p_compile_unit(p):
	'''compilationUnit  : package_units_opt topStatSeq '''

def p_package_units_opt(p):
	'''package_units_opt : package_units | empty '''

def p_package_units(p):
	''' package_units :  package_unit | package_units package_unit '''

def p_package_unit(p)
	''' package_unit : TOK_package qualid TOK_SEMICOLON | empty '''

'''
packageObject
   : 'package' 'object' objectDef
   ;
'''

def p_package_object(p):
	''' packageObject : TOK_package TOK_object objectdef'''



'''
packaging
   : 'package' qualId '{' topStatSeq '}'
   ;
'''

def p_packaging(p):
	''' packaging : TOK_package qualid TOK_LPAREN topStatSeq TOK_RPAREN '''


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
	''' topStat : annotations_opt modifiers_opt tmplDef | import_ | packaging | packageObject '''

def p_annotations_opt(p):
	''' annotations_opt :  annotations | empty '''	

def p_annotations(p):
	''' annotations : annotation | annotations annotation '''

def p_modifiers_opt(p):
	'''modifiers_opt : modifiers | empty '''

def p_modifiers(p):
	''' modifiers : modifier | modifiers modifier | empty '''


'''
topStatSeq
   : topStat (Semi topStat)*
   ;
'''
def p_topStatSeq(p):
	''' topstatSeq : topStat Semi_topStats_opt '''

def p_Semi_topStats(p):
	''' SemitopStats_opt : SemitopStats | empty'''

def p_Semi_topStats(p):
	''' Semi_topStats : Semi_topStat | Semi_topStats Semi_topStat'''

def p_Semi_topStat(p):
	''' Semi_topStat : TOK_SEMICOLON topStat '''


'''
selfInvocation
   : 'this' argumentExprs +
   ;
'''

def p_selfInvocation(p):
	''' selfInvocation : TOK_this argumentExprss'''

#defined here but not used in this rule
def p_argumentExprss_opt(p):
	''' argumentExprss_opt : argumentExprss | empty '''

def p_argumentExprss(p):
	''' argumentExprss : argumentExprs | argumentExprss argumentExprs'''



'''
constrBlock
   : '{' selfInvocation (Semi blockStat)* '}'
   ;
'''

def p_constrBlock(p):
	''' constrBlock : TOK_LPAREN selfInvocation Semi_blockStats_opt TOK_RPAREN '''

def p_Semi_blockStats_opt(p):
	''' Semi_blockStats_opt : Semi_blockStats | empty'''

def p_Semi_blockStats(p):
	''' Semi_blockStats : Semi_blockStat | Semi_blockStats Semi_blockStat '''

def p_Semi_blockStat(p):
	'''Semi_blockStat : TOK_SEMICOLON blockStat'''


'''
constrExpr
   : selfInvocation
   | constrBlock
   ;
'''
def p_constrExpr(p):
	''' constrExpr : selfInvocation | constrBlock'''


'''
earlyDef
   : (annotation)* modifier* patVarDef
   ;
'''
#annotations and modifiers defined beforehand
def p_earlyDef(p):
	''' earlyDef : annotations_opt modifiers_opt patVarDef '''


'''
earlyDefs
   : '{' (earlyDef (Semi earlyDef)*)? '}' 'with'
   ;
'''

def p_earlyDefs(p):
	''' earlyDefs : TOK_LPAREN empty TOK_RPAREN TOK_with | TOK_LPAREN earlyDef Semi_earlyDefs_opt TOK_RPAREN TOK_with '''

def p_Semi_earlyDefs_opt(p):
	''' Semi_earlyDefs_opt : Semi_earlyDefs | empty '''

def p_Semi_earlyDefs(p):
	''' Semi_earlyDefs : Semi_earlyDef | Semi_earlyDefs Semi_earlyDef '''

def p_Semi_earlyDef(p):
	''' Semi_earlyDef : TOK _SEMICOLON earlyDef '''


'''
constr
   : annotType argumentExprs*
   ;
'''

def p_constr(p):
	''' constr : annotType arguementsExprss_opt'''

'''
traitParents
   : annotType ('with' annotType)*
   ;
'''
def p_traitParents(p):
	''' traitParents : annotType with_annotTypes_opt '''

def p_with_annotTypes_opt(p):
	''' with_annotTypes_opt : with_annotTypes | empty '''

def p_with_annotTypes(p):
	'''with_annotTypes : with_annotType | with_annotTypes with_annotType '''

def p_with_annotType(p):
	'''with_annotType : TOK_with annotType'''

'''
classParents
   : constr ('with' annotType)*
   ;

'''
def p_classParents(p):
	''' classParents : constr with_annotTypes_opt'''


'''
traitTemplate
   : earlyDefs? traitParents templateBody?
   ;
'''
def p_traitTemplate(p):
	''' traitTemplate : traitParents | traitParents templateBody |  earlyDefs traitParents | earlyDefs traitParents templateBody'''

'''
classTemplate
   : earlyDefs? classParents templateBody?
   ;
'''
def p_classTemplate(p):
	''' classTemplate : classParents | classParents templateBody |  earlyDefs classParents | earlyDefs classParents templateBody'''

'''
traitTemplateOpt
   : 'extends' traitTemplate
   | ('extends'? templateBody)?
   ;
'''
def p_traitTemplateOpt(p):
	''' traitTemplateOpt : TOK_extends traitTemplate | TOK_extends templateBody | templateBody | empty'''

'''
classTemplateOpt
   : 'extends' classTemplate
   | ('extends'? templateBody)?
   ;
'''
def p_classTemplateOpt(p):
	''' classTemplateOpt : TOK_extends classTemplate | TOK_extends templateBody | templateBody | empty'''


'''
objectDef
   : Id classTemplateOpt
   ;
'''

def p_objectDef(p):
	''' objectDef : Id classTemplateOpt'''

'''
traitDef
   : Id typeParamClause? traitTemplateOpt
   ;
'''
def p_traitDef(p):
	''' traitDef : Id traitTemplateOpt | Id typeParamClause traitTemplateOpt'''


'''
classDef
   : Id typeParamClause? constrAnnotation* accessModifier? classParamClauses classTemplateOpt
   ;
'''

def p_classDef(p):
	''' classDef : Id constrAnnotations_opt classParamClauses classTemplateOpt | Id constrAnnotations_opt accessModifier classParamClauses classTemplateOpt | Id typeParamClause constrAnnotations_opt  classParamClauses classTemplateOpt | Id typeParamClause constrAnnotations_opt accessModifier classParamClauses classTemplateOpt '''

def p_constrAnnotations_opt(p):
	''' constrAnnotations_opt : constrAnnotations | empty '''

def p_constrAnnotations(p):
	''' constrAnnotations : constrAnnotation | constrAnnotations constrAnnotation '''

'''
tmplDef
   : 'case'? 'class' classDef
   | 'case' 'object' objectDef
   | 'trait' traitDef
   ;
'''
def p_tmplDef(p):
	''' tmplDef    : TOK_class classDef | TOK_case TOK_class classDef    | TOK_case TOK_object objectDef | TOK_trait traitDef '''


'''
typeDef
   : Id typeParamClause? '=' type
   ;
'''
def p_typeDef(p):
	''' typeDef :  Id TOK_ASSIGN type | Id typeParamClause TOK_ASSIGN type '''


'''
funDef
   : funSig (':' type)? '=' expr
   | funSig '{' block '}'
   | 'this' paramClause paramClauses ('=' constrExpr | constrBlock)
   ;
'''

def p_funDef(p):
	''' funDef : funSig TOK_ASSIGN expr | funSig TOK_COLON type TOK_ASSIGN expr   | funSig TOK_LPAREN block TOK_RPAREN | TOK_this paramClause paramClauses TOK_ASSIGN constrExpr | TOK_this paramClause paramClauses constrBlock'''


'''
varDef
   : patDef
   | ids ':' type '=' '_'
   ;
'''

def p_varDef(p):
	'''varDef   : patDef | ids TOK_COLON type TOK_ASSIGN TOK_UNDERSCORE '''	


'''
patDef
   : pattern2 (',' pattern2)* (':' type)* '=' expr
   ;
'''
def p_patDef(p):
	'''patDef : pattern2 TOK_COMMA_pattern2s_opt TOK_COLON_types_opt TOK_ASSIGN expr '''


def p_TOK_COMMA_pattern2s_opt(p):
	''' TOK_COMMA_pattern2s_opt : TOK_COMMA_pattern2s | empty '''

def p_TOK_COMMA_pattern2s(p):
	''' TOK_COMMA_pattern2s : TOK_COMMA_pattern2 | TOK_COMMA_pattern2s TOK_COMMA_pattern2 '''

def TOK_COMMA_pattern2(p):
	''' TOK_COMMA_pattern2 : TOK_COMMA pattern2 '''



def p_TOK_COLON_types_opt(p):
	''' TOK_COLON_types_opt : TOK_COLON_types | empty '''

def p_TOK_COLON_types(p):
	''' TOK_COLON_types : TOK_COLON_type | TOK_COLON_types TOK_COLON_type '''

def p_TOK_COLON_type(p):
	''' TOK_COLON_type : TOK_COLON type '''


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


'''
patVarDef
   : 'val' patDef
   | 'var' varDef
   ;
'''
def p_patVarDef(p):
	''' patVarDef : TOK_VAL patDef | TOK_VAR varDef '''


'''
typeDcl
   : Id typeParamClause? ('>:' type)? ('<:' type)?
   ;
'''
def p_typeDcl(p):
	''' typeDcl : Id | Id TOK_LT_COLON type | Id TOK_GT_COLON type | Id TOK_GT_COLON type TOK_LT_COLON type | Id typeParamClause | Id typeParamClause TOK_LT_COLON type | Id typeParamClause TOK_GT_COLON type | Id typeParamClause TOK_GT_COLON type TOK_LT_COLON type '''


'''
funSig
   : Id funTypeParamClause? paramClauses
'''

def p_funSig(p):
	''' funSig : Id paramClauses | Id funTypeParamClause paramClauses '''

'''
funDcl
   : funSig (':' type)?
   ;
'''

def p_funDcl(p):
	''' funDcl  : funSig | funSig TOK_COLON_type '''


'''
varDcl
   : ids ':' type
   ;
'''

def p_varDcl(p):
	'''varDcl : ids TOK_COLON type '''


'''
valDcl
   : ids ':' type
   ;
'''

def p_valDcl(p):
	''' valDcl : ids TOK_COLON type'''

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


'''
importSelector
   : Id ('=>' Id | '=>' '_')
   ;
'''

def p_importSelector(p):
	''' importSelector  : Id TOK_EQ_GT TOK_UNDERSCORE | Id TOK_EQ_GT Id '''
	
