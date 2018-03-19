grammar Scala;

literal
   : '-'? IntegerLiteral
   | '-'? FloatingPointLiteral
   | BooleanLiteral
   | CharacterLiteral
   | StringLiteral
   | SymbolLiteral
   | 'null'
   ;

qualId
   : Id ('.' Id)*
   ;

ids
   : Id (',' Id)*
   ;

stableId
   : (Id | (Id '.')? 'this') '.' Id
   | (Id '.')? 'super' classQualifier? '.' Id
   ;

classQualifier
   : '[' Id ']'
   ;

type
   : functionArgTypes '=>' type
   | infixType existentialClause?
   ;

functionArgTypes
   : infixType
   | '(' (paramType (',' paramType)*)? ')'
   ;

existentialClause
   : 'forSome' '{' existentialDcl (Semi existentialDcl)* '}'
   ;

existentialDcl
   : 'type' typeDcl
   | 'val' valDcl
   ;

infixType
   : compoundType (Id compoundType)*
   ;

compoundType
   : annotType ('with' annotType)* refinement?
   | refinement
   ;

annotType
   : simpleType annotation*
   ;

simpleType
   : simpleType typeArgs
   | simpleType '#' Id
   | stableId
   | (stableId | (Id '.')? 'this') '.' 'type'
   | '(' types ')'
   ;

typeArgs
   : '[' types ']'
   ;

types
   : type (',' type)*
   ;

refinement
   : '{' refineStat (Semi refineStat)* '}'
   ;

refineStat
   : dcl
   | 'type' typeDef
   |
   ;

typePat
   : type
   ;

ascription
   : ':' infixType
   | ':' annotation +
   | ':' '_' '*'
   ;

expr
   : (bindings | 'implicit'? Id | '_') '=>' expr
   | expr1
   ;

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

postfixExpr
   : infixExpr (Id)?
   ;

infixExpr
   : prefixExpr
   | infixExpr Id infixExpr
   ;

prefixExpr
   : ('-' | '+' | '~' | '!')? ('new' (classTemplate | templateBody) | blockExpr | simpleExpr1 '_'?)
   ;

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

exprs
   : expr (',' expr)*
   ;

argumentExprs
   : '(' exprs? ')'
   | '(' (exprs ',')? postfixExpr ':' '_' '*' ')'
   | blockExpr
   ;

blockExpr
   : '{' caseClauses '}'
   | '{' block '}'
   ;

block
   : blockStat (Semi blockStat)* resultExpr?
   ;

blockStat
   : import_
   | annotation* ('implicit' | 'lazy')? def
   | annotation* localModifier* tmplDef
   | expr1
   |
   ;

resultExpr
   : expr1
   | (bindings | ('implicit'? Id | '_') ':' compoundType) '=>' block
   ;

enumerators
   : generator (Semi generator)*
   ;

generator
   : pattern1 '<-' expr (Semi? guard | Semi pattern1 '=' expr)*
   ;

caseClauses
   : caseClause +
   ;

caseClause
   : 'case' pattern guard? '=>' block
   ;

guard
   : 'if' postfixExpr
   ;

pattern
   : pattern1 ('|' pattern1)*
   ;

pattern1
   : Varid ':' typePat
   | '_' ':' typePat
   | pattern2
   ;

pattern2
   : Varid ('@' pattern3)?
   | pattern3
   ;

pattern3
   : simplePattern
   | simplePattern (Id simplePattern)*
   ;

simplePattern
   : '_'
   | Varid
   | literal
   | stableId ('(' patterns? ')')?
   | stableId '(' (patterns? ',')? (Varid '@')? '_' '*' ')'
   | '(' patterns? ')'
   ;

patterns
   : pattern (',' pattern)*
   | '_'+
   ;

typeParamClause
   : '[' variantTypeParam (',' variantTypeParam)* ']'
   ;

funTypeParamClause
   : '[' typeParam (',' typeParam)* ']'
   ;

variantTypeParam
   : annotation? ('+' | '-')? typeParam
   ;

typeParam
   : (Id | '_') typeParamClause? ('>:' type)? ('<:' type)? ('<%' type)* (':' type)*
   ;

paramClauses
   : paramClause* ('(' 'implicit' params ')')?
   ;

paramClause
   : '(' params? ')'
   ;

params
   : param (',' param)*
   ;

param
   : annotation* Id (':' paramType)? ('=' expr)?
   ;





