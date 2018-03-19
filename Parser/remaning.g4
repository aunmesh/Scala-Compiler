grammar Scala;



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




