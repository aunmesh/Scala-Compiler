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
	''' package_unit : TOK_package qualid TOK_SEMICOLON '''

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


'''
importSelectors
   : '{' (importSelector ',')* (importSelector | '_') '}'
   ;
'''

def p_importSelectors(p):
	''' importSelectors : TOK_LPAREN importSelector_TOK_COMMAs_opt importSelector TOK_RPAREN | TOK_LPAREN importSelector_TOK_COMMAs_opt  TOK_UNDERSCORE TOK_RPAREN'''

def p_importSelector_TOK_COMMAs_opt(p):
	'''importSelector_TOK_COMMAs_opt : importSelector_TOK_COMMAs | empty '''

def importSelector_TOK_COMMAs(p);
	'''importSelector_TOK_COMMAs : importSelector_TOK_COMMA | importSelector_TOK_COMMAs importSelector_TOK_COMMA '''

def importSelector_TOK_COMMA(p):
	''' importSelector_TOK_COMMA : importSelector TOK_COMMA'''

'''
importExpr
   : stableId '.' (Id | '_' | importSelectors)
   ;
'''

def p_importExpr(p):
	''' importExpr  : stableId TOK_DOT Id | stableId TOK_DOT TOK_UNDERSCORE  | stableId TOK_DOT importSelectors '''


'''
import_
   : 'import' importExpr (',' importExpr)*
   ;
'''

def p_import_(p);
	''' import_ : TOK_import importExpr TOK_COMMA_importExprs_opt '''

def p_TOK_COMMA_importExprs_opt(p):
	''' TOK_COMMA_importExprs_opt : TOK_COMMA_importExprs | empty '''

def p_TOK_COMMA_importExprs(p):
	''' TOK_COMMA_importExprs : TOK_COMMA_importExpr | TOK_COMMA_importExprs TOK_COMMA_importExpr '''

def p_TOK_COMMA_importExpr(p):
	'''TOK_COMMA_importExpr : TOK_COMMA importExpr'''


'''
selfType
   : Id (':' type)? '=>'
   | 'this' ':' type '=>'
   ;
'''

def p_selfType(p):
	''' selfType : Id TOK_EQ_GT | Id  TOK_COLON type TOK_EQ_GT | TOK_this TOK_COLON type TOK_EQ_GT'''


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
	''' templateStat : import_  | annotations_opt modifiers_opt def  | annotations_opt modifiers_opt dcl | expr | empty '''

'''
templateBody
   : '{' selfType? templateStat (Semi templateStat)* '}'
   ;
'''
def p_templateBody(p):
	''' templateBody : TOK_LPAREN templateStat TOK_SEMICOLON_templateStats_opt TOK_RPAREN 
	| TOK_LPAREN selfType templateStat TOK_SEMICOLON_templateStats_opt TOK_RPAREN '''

def p_TOK_SEMICOLON_templateStats_opt(p):
	''' TOK_SEMICOLON_templateStats_opt : TOK_SEMICOLON_templateStats | empty '''

def p_TOK_SEMICOLON_templateStats(p):
	''' TOK_SEMICOLON_templateStats : TOK_SEMICOLON_templateStat | TOK_SEMICOLON_templateStats TOK_SEMICOLON_templateStat '''

def p_TOK_SEMICOLON_templateStat(p):
	''' TOK_SEMICOLON_templateStat : TOK_SEMICOLON templateStat '''


'''
constrAnnotation
   : '@' simpleType argumentExprs
   ;
'''

def p_constrAnnotation(p):
	'''constrAnnotation : TOK_AT simpleType argumentExprs '''
	

'''
annotation
   : '@' simpleType argumentExprs*
   ;
'''

def p_annotation(p):
	'''annotation   : TOK_AT simpleType argumentExprss_opt :'''

'''
accessQualifier
   : '[' (Id | 'this') ']'
   ;
'''

def p_accessQualifier(p):
	''' accessQualifier  : TOK_LSQB Id TOK_RSQB | TOK_LSQB  TOK_this TOK_RSQB '''

'''
accessModifier
   : ('private' | 'protected') accessQualifier?
   ;
'''

def p_accessModifier(p);
	'''accessModifier : TOK_private | TOK_private accessQualifier | TOK_protected | TOK_protected accessQualifier '''

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
	''' localModifier   : TOK_abstract   | TOK_final   | TOK_sealed   | TOK_implicit  | TOK_lazy	'''

'''
modifier
   : localModifier
   | accessModifier
   | 'override'
   ;
'''

def p_modifier(p):
	'''modifier : localModifier | accessModifier | TOK_override '''

'''
binding
   : (Id | '_') (':' type)?
   ;
'''
def p_binding(p):
	'''binding   : '_' | Id | Id TOK_COLON_type | TOK_UNDERSCORE TOK_COLON_type  '''

'''
bindings
   : '(' binding (',' binding)* ')'
   ;
'''	
def p_bindings(p):
	'''bindings   : TOK_LPAREN binding TOK_COMMA_bindings_opt TOK_RPAREN '''

def p_TOK_COMMA_bindings_opt(p):
	''' TOK_COMMA_bindings_opt : TOK_COMMA_bindings | empty '''

def p_TOK_COMMA_bindings(p):
	''' TOK_COMMA_bindings : TOK_COMMA_binding | TOK_COMMA_bindings TOK_COMMA_binding '''

def p_TOK_COMMA_binding(p):
	''' TOK_COMMA_binding : TOK_COMMA bindings '''

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


'''
classParams
   : classParam (',' classParam)*
   ;
'''
def p_classParams(p):
	'''classParams   : classParam (',' classParam)* '''

def p_TOK_COMMA_classParams_opt(p):
	'''TOK_COMMA_classParams_opt : TOK_COMMA_classParams | empty'''

def p_TOK_COMMA_classParams(p):
	''' TOK_COMMA_classParams : TOK_COMMA_classParam | TOK_COMMA_classParams TOK_COMMA_classParam '''

def p_TOK_COMMA_classParam(p):
	''' TOK_COMMA_classParams : TOK_COMMA classParams'''
	 

'''
classParamClause
   : '(' classParams? ')'
   ;
'''

def p_classParamClause(p):
	'''classParamClause   : TOK_LPAREN TOK_RPAREN | TOK_LPAREN classParams TOK_RPAREN  '''

'''
classParamClauses
   : classParamClause* ('(' 'implicit' classParams ')')?
   ;
'''

def p_classParamClauses(p):
	'''
	classParamClauses  : classParamClauses_opt | classParamClauses_opt TOK_LPAREN TOK_implicit classParams TOK_RPAREN '''

def p_classParamClauses_opt(p):
	''' classParamClauses_opt : classParamClauses | empty '''

def p_classParamClauses(p):
	''' classParamClauses : classParamClause | classParamClause classParamClauses '''

'''
paramType
   : type
   | '=>' type
   | type '*'
   ;
'''
def p_paramType(p):
	''' paramType : type | TOK_EQ_GT type	 | type TOK_STAR'''



'''
param
   : annotation* Id (':' paramType)? ('=' expr)?
   ;
'''
def p_param(p):
	'''param   : annotations_opt Id | annotations_opt Id TOK_ASSIGN expr | annotations_opt Id TOK_COLON paramType  | annotations_opt Id TOK_COLON paramType TOK_ASSIGN expr '''
	
def p_TOK_COLON_paramTypes_opt(p):
	''' TOK_COLON_paramTypes_opt : TOK_COLON_paramTypes | empty '''

def p_TOK_COLON_paramTypes(p):
	''' TOK_COLON_paramTypes : TOK_COLON_paramType | TOK_COLON_paramTypes TOK_COLON_paramType '''

def p_TOK_COLON_paramType(p):
	''' TOK_COLON_paramType : TOK_COLON paramTypes '''


'''
params
   : param (',' param)*
   ;
'''

def p_params(p):
	'''params   : param TOK_COMMA_params_opt  '''
	

def p_TOK_COMMA_params_opt(p):
	''' TOK_COMMA_params_opt : TOK_COMMA_params | empty '''

def p_TOK_COMMA_params(p):
	''' TOK_COMMA_params : TOK_COMMA_param | TOK_COMMA_param TOK_COMMA_params '''

def p_TOK_COMMA_param(p):
	''' TOK_COMMA_param : TOK_COLON param '''


'''
paramClause
   : '(' params? ')'
   ;
'''
def p_paramClause(p):
	'''paramClause   : TOK_LPAREN TOK_RPAREN | TOK_LPAREN params TOK_RPAREN'''
	
'''
paramClauses
   : paramClause* ('(' 'implicit' params ')')?
   ;
'''
def p_paramClauses(p):
	''' paramClauses   : paramClauses_opt | paramClauses_opt TOK_LPAREN TOK_implicit params TOK_RPAREN  '''



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
	'''literal : TOK_MINUS IntegerLiteral | IntegerLiteral | FloatingPointLiteral | TOK_MINUS FloatingPointLiteral   | BooleanLiteral 
	| CharacterLiteral | StringLiteral | SymbolLiteral | TOK_null'''

'''
qualId
   : Id ('.' Id)*
   ;
'''
def p_qualId(p):
	'''qualId   : Id TOK_DOT_Ids_opt '''

def p_TOK_DOT_Ids_opt(p):
	'''  TOK_DOT_Ids_opt : TOK_DOT_Ids | empty '''

def p_TOK_DOT_Ids(p):
	''' TOK_DOT_Ids : TOK_DOT_Id | TOK_DOT_Ids TOK_DOT_Id '''

def TOK_DOT_Id(p)
	''' TOK_DOT_Id : TOK_DOT Id '''


'''
ids
   : Id (',' Id)*
   ;
'''
def p_ids(p):
	'''ids : Id TOK_COMMA_Ids_opt '''

def p_TOK_COMMA_Ids_opt(p):
	'''  TOK_COMMA_Ids_opt : TOK_COMMA_Ids | empty '''

def p_TOK_COMMA_Ids(p):
	''' TOK_COMMA_Ids : TOK_COMMA_Id | TOK_COMMA_Ids TOK_COMMA_Id '''

def TOK_COMMA_Id(p)
	''' TOK_COMMA_Id : TOK_COMMA Id '''

	
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
	
'''
classQualifier
   : '[' Id ']'
   ;
'''
def p_classQualifier(p):
	'''classQualifier  : TOK_LSQB Id TOK_RSQB '''

'''
type
   : functionArgTypes '=>' type
   | infixType existentialClause?
   ;
'''
def p_type(p):
	'''type  : functionArgTypes TOK_EQ_GT type  | infixType | infixType existentialClause  '''

'''
functionArgTypes
   : infixType
   | '(' (paramType (',' paramType)*)? ')'
   ;
'''
def p_functionArgTypes(p):
	'''functionArgTypes   : infixType   | TOK_LPAREN TOK_RPAREN | TOK_LPAREN paramType TOK_COMMA_paramTypes_opt TOK_RPAREN '''


def p_TOK_COMMA_paramTypes_opt(p):
	''' TOK_COMMA_paramTypes_opt : TOK_COMMA_paramTypes | empty '''

def p_TOK_COMMA_paramTypes(p):
	''' TOK_COMMA_paramTypes : TOK_COMMA_paramType | TOK_COMMA_paramTypes TOK_COMMA_paramType '''

def p_TOK_COMMA_paramType(p):
	''' TOK_COMMA_paramType : TOK_COMMA paramType '''

'''
existentialClause
   : 'forSome' '{' existentialDcl (Semi existentialDcl)* '}'
   ;
'''
def p_existentialClause(p):
	'''existentialClause  : TOK_forSome TOK_LCUR existentialDcl (Semi existentialDcl)* TOK_RCUR  '''

def p_TOK_SEMICOLON_existentialDcls_opt(p):
	''' TOK_SEMICOLON_existentialDcls_opt : TOK_SEMICOLON_existentialDcls | empty '''

def p_TOK_SEMICOLON_existentialDcls(p):
	''' TOK_SEMICOLON_existentialDcls : TOK_SEMICOLON_existentialDcl | TOK_SEMICOLON_existentialDcls TOK_SEMICOLON_existentialDcl '''

def p_TOK_SEMICOLON_existentialDcl(p):
	''' TOK_SEMICOLON_existentialDcl : TOK_SEMICOLON existentialDcl '''
	

'''
existentialDcl
   : 'type' typeDcl
   | 'val' valDcl
   ;
'''
def p_existentialDcl(p):
	'''existentialDcl  : TOK_type typeDcl  | TOK_val valDcl '''

'''
infixType
   : compoundType (Id compoundType)*
   ;
'''
def p_infixType(p):
	'''infixType   : compoundType (Id compoundType)* '''

def p_id_compoundTypes_opt(p):
	''' id_compoundTypes_opt : id_compoundTypes | empty '''

def p_id_compoundTypes(p):
	''' id_compoundTypes : id_compoundType | id_compoundTypes id_compoundTypes '''

def p_id_compoundType(p):
	''' id_compoundType : id compoundType '''

'''
compoundType
   : annotType ('with' annotType)* refinement?
   | refinement
   ;
'''

def p_compoundType(p):
	'''compoundType   : annotType TOK_with_annotTypes_opt | annotType TOK_with_annotTypes_opt refinement  | refinement '''

def p_TOK_with_annotTypes_opt(p):
	''' TOK_with_annotTypess_opt : TOK_with_annotTypes | empty '''

def p_TOK_with_annotTypes(p):
	''' TOK_with_annotTypes : TOK_with_annotType | TOK_with_annotTypes TOK_with_annotType '''

def p_TOK_with_annotType(p):
	''' TOK_with_annotType : TOK_with annotType '''


'''
annotType
   : simpleType annotation*
   ;
'''
#annotations_opt defined beforehand
def p_annotType(p):
	'''annotType : simpleType annotations_opt '''


'''
simpleType
   : simpleType typeArgs
   | simpleType '#' Id
   | stableId
   | (stableId | (Id '.')? 'this') '.' 'type'
   | '(' types ')'
   ;
'''
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

'''
types
   : type (',' type)*
   ;
'''
def p_types(p):
	'''types  : type TOK_COMMA_types_opt '''


def p_TOK_COMMA_types_opt(p):
	''' TOK_COMMA_types_opt : TOK_COMMA_types | empty '''

def p_TOK_COMMA_types(p):
	''' TOK_COMMA_types : TOK_COMMA_type | TOK_COMMA_types TOK_COMMA_type '''

def p_TOK_COMMA_type(p):
	''' TOK_COMMA_type : TOK_COMMA type '''


'''
refinement
   : '{' refineStat (Semi refineStat)* '}'
   ;
'''

def p_refinement(p):
	''' refinement   : TOK_LCUR refineStat TOK_SEMICOLON_refineStats_opt TOK_RCUR '''

def p_TOK_SEMICOLON_refineStats_opt(p):
	''' TOK_SEMICOLON_refineStats_opt : TOK_SEMICOLON_refineStats | empty '''

def p_TOK_SEMICOLON_refineStats(p):
	''' TOK_SEMICOLON_refineStats : TOK_SEMICOLON_refineStat | TOK_SEMICOLON_refineStats TOK_SEMICOLON_refineStat '''

def p_TOK_SEMICOLON_refineStat(p):
	''' TOK_SEMICOLON_refineStat : TOK_SEMICOLON refineStat '''

'''
refineStat
   : dcl
   | 'type' typeDef
   |
   ;
'''
def p_refineStat(p):
	'''refineStat   : dcl   | TOK_type typeDef   |  empty 	'''


'''
typePat
   : type
   ;
'''
def p_typePat(p):
	''' typePat : type  '''
	

'''
ascription
   : ':' infixType
   | ':' annotation +
   | ':' '_' '*'
   ;
'''
def p_ascription(p):
	'''ascription  : TOK_COLON infixType   | TOK_COLON annotations   | TOK_COLON TOK_UNDERSCORE TOK_STAR  '''

'''
expr
   : (bindings | 'implicit'? Id | '_') '=>' expr
   | expr1
   ;
'''
def p_expr(p):
	'''expr  : temp TOK_EQ_GT expr   | expr1 '''

def p_temp(p):
	''' temp : bindings | TOK_implicit Id | Id | TOK_UNDERSCORE'''


'''
expr1
   : 'if' '(' expr ')' expr (Semi? 'else' expr)?

   | 'while' '(' expr ')' expr

   | 'try' ('{' block '}' | expr) ('catch' '{' caseClauses '}')? ('finally' expr)?

   | 'do' expr Semi? 'while' '(' expr ')'

   | 'for' ('(' enumerators ')' | '{' enumerators '}') 'yield'? expr

   | 'throw' expr

   | 'return' expr?

   | (('new' (classTemplate | templateBody) | blockExpr | simpleExpr1 '_'?) '.') Id '=' expr

   | simpleExpr1 argumentExprs '=' expr

   | postfixExpr
   | postfixExpr ascription
   | postfixExpr 'match' '{' caseClauses '}'
   ;
'''
def p_expr1(p):
	''' expr1 : if_expr | while_expr | try_expr | do_expr | for_expr | throw_expr | return_expr | new_expr | special_expr | postfix_expr1'''




'''
if_expr :  'if' '(' expr ')' expr (Semi? 'else' expr)?
'''
def p_if_expr(p):
	'''if_expr :  TOK_if TOK_LAPREN expr TOK_RPAREN expr | TOK_if TOK_LAPREN expr TOK_RPAREN expr TOK_else expr | TOK_if TOK_LAPREN expr TOK_RPAREN expr 		TOK_SEMICOLON TOK_else expr '''


'''
while_expr:   'while' '(' expr ')' expr
'''
def p_while_expr(p):
	''' while_expr:   TOK_while TOK_LAPREN expr TOK_RPAREN expr	'''

'''
try_expr:   'try' ('{' block '}' | expr) ('catch' '{' caseClauses '}')? ('finally' expr)?
'''
def p_try_expr(p):
	'''	try_expr:   TOK_try temp2 |  TOK_try temp2 temp3 | TOK_try temp2 temp4 | TOK_try temp2 temp3 temp4'''
	

def p_temp2(p):
	''' temp2 : TOK_LCUR block TOK_RCUR | expr '''

def p_temp3(p):
	'''temp3 : TOK_catch TOK_LCUR caseClauses TOK_RCUR'''

def p_temp4(p):
	''' temp4 : TOK_finally expr '''

'''
do_expr:   'do' expr Semi? 'while' '(' expr ')'
'''
def p_do_expr(p);
	'''	do_expr:   TOK_do expr TOK_SEMICOLON TOK_while TOK_LPAREN expr TOK_RPAREN	'''


'''
for_expr:   'for' ('(' enumerators ')' | '{' enumerators '}') 'yield'? expr
'''
def p_for_expr(p):
	'''	for_expr:   TOK_for temp5 expr | TOK_for temp5 TOK_yield expr 	'''

def p_temp5(p):
	''' temp5: TOK_LPAREN enumerators TOK_RPAREN | TOK_LCUR enumerators TOK_RCUR '''


'''
throw_expr:   'throw' expr
'''
def p_throw_expr(p):
	''' throw_expr:   TOK_throw expr '''

'''
return_expr :   'return' expr?
'''
def p_return_expr(p):
	'''	return_expr :   TOK_return | TOK_return expr 	'''
	

'''
new_expr :   (('new' (classTemplate | templateBody) | blockExpr | simpleExpr1 '_'?) '.') Id '=' expr
'''
def p_new_expr(p):
	'''new_expr :  temp59 TOK_DOT Id TOK_ASSIGN expr '''

def p_temp55(p):
	'''temp55 : classTemplate | templateBody '''
def p_temp59(p):
	'''temp6 : TOK_new temp55 | blockExpr | simpleExpr1 | simpleExpr1 TOK_UNDERSCORE '''

'''
special_expr :   simpleExpr1 argumentExprs '=' expr
'''
def p_special_expr(p):
	'''special_expr :  simpleExpr1 argumentExprs TOK_ASSIGN expr '''


'''
postfix_expr :   postfixExpr  | postfixExpr ascription  | postfixExpr 'match' '{' caseClauses '}'
'''
def p_postfix_expr1(p):
	'''	postfix_expr1 :   postfixExpr  | postfixExpr ascription  | postfixExpr TOK_match TOK_LCUR caseClauses TOK_RCUR	'''





'''
postfixExpr
   : infixExpr (Id)?
   ;
'''
def p_postfixExpr(p):
	'''postfixExpr  : infixExpr | infixExpr Id'''

'''
infixExpr
   : prefixExpr
   | infixExpr Id infixExpr
   ;
'''
def p_infixExpr
	''' infixExpr  : prefixExpr  | infixExpr Id infixExpr '''


'''
prefixExpr
   : ('-' | '+' | '~' | '!')? ('new' (classTemplate | templateBody) | blockExpr | simpleExpr1 '_'?)
   ;
'''
def p_prefixExpr(p):
	'''prefixExpr  : temp6 | temp7 | temp8 temp6 | temp8 temp7 '''


def p_temp6(p):
	'''temp6 : TOK_new classTemplate | blockExpr | simpleExpr1 | simpleExpr1 TOK_UNDERSCORE '''


def p_temp7(p):
	'''temp6 : TOK_new templateBody | blockExpr | simpleExpr1 | simpleExpr1 TOK_UNDERSCORE '''


def p_temp8(p):
	''' temp8 : TOK_MINUS | TOK_PLUS | TOK_TILDA | TOK_EXCLAIM '''


'''
simpleExpr1
   : literal
   | stableId
   | (Id '.')? 'this'
   | '_'
   | '(' exprs? ')'
   | ('new' (classTemplate | templateBody) | blockExpr) '.' Id
   | ('new' (classTemplate | templateBody) | blockExpr) typeArgs
   | simpleExpr1 argumentExprs
   ;
'''


