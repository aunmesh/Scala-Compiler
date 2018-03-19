# -*- coding: utf-8 -*-

'''
Corrections for parseer:
String
Identifier
'''

'''
Verify if regex is present for all of these
LEAVES = {		'OR','AND','OR_BITWISE','AND_BITWISE','XOR','EqualityOp',
			'RelationalOp','ShiftOp','AddOp','Multop','Unary10p','UnaryOp'
			'LPAREN_Done','RPAREN_Done',
			'LiteralConst','IntFloatConst',
			'TOK_COMMA','ModifierKeyword',
			'STATE_END','FUNTYPE',
			'ARRAY','DOT',
			'INT_CONST'
			'CHOOSE','UNTIL_TO','BY','VOID','DEF','empty','TOK_ASSIGN','ASSIGN_OP','OFDIM'
			}
'''

from ply import lex as lex
import re,sys
from test import *

#List of token names. Always required
#TOKEN NAMES IN SCALA
'''
1 Identifiers
2 Newline Characters
3 LITs
1 Integer LITs
2 Floating Point LITs
3 Boolean LITs
4 Character LITs
5 String LITs
6 Escape Sequences
7 Symbol LITs
4 Whitespace and Comments
5 Trailing Commas in Multi-line Expressions
6 XML mode
'''
keywords = {

     'abstract' : 'TOK_abstract',
     'case' : 'TOK_case',	
     'catch' : 'TOK_catch',
     'class' : 'TOK_class',
     'def' : 'TOK_def',
     'do' : 'TOK_do',
     'else' : 'TOK_else',
     'extends' : 'TOK_extends',
     'false' : 'TOK_false',
     'final' : 'TOK_final',
     'finally' : 'TOK_finally',
     'for' : 'TOK_for',
     'forSome' : 'TOK_forSome',
     'if' : 'TOK_if',
     'implicit' : 'TOK_implicit',
     'import' : 'TOK_import',
     'lazy' : 'TOK_lazy',
     'match' : 'TOK_match',
     'new' : 'TOK_new',
     'null' : 'TOK_null',
     'object' : 'TOK_object',
     'override' : 'TOK_override',
     'package' : 'TOK_package',
     'private' : 'TOK_private',
     'protected' : 'TOK_protected',
     'return' : 'TOK_return',
     'sealed' : 'TOK_sealed',
     'super' : 'TOK_super',
     'this' : 'TOK_this',
     'throw' : 'TOK_throw',
     'trait' : 'TOK_trait',
     'Try' : 'TOK_Try',
     'true' : 'TOK_true',
     'type' : 'TOK_type',
     'until' : 'TOK_until',
     'to' : 'TOK_TO',
     'ofDim'  :  'TOK_OFDIM',
     'val' : 'TOK_val',
     'Var' : 'TOK_var',
     'while' : 'TOK_while',
     'with' : 'TOK_with',
     'yield' : 'TOK_yield',
}


#THESE ARE NOT KEYWORDS BUT OPERATORS, INCLUDED IN REGULAR EXPRESSIONS BELOW
'''
     '-' : 'TOK_MINUS',
     ':' : 'TOK_COLON',
     '=' : 'TOK_EQ',
     '=>' : 'TOK_EQ_GT',
     '<-' : 'TOK_LT_MINUS',
     '<:' : 'TOK_LE_COLON',
     '<%' : 'TOK_LT_PERCENT',
     '>:' : 'TOK_GT_COLON',
     '#' : 'TOK_HASH',
     '@' : "TOK_AT",
     ',' : "TOK_COMMA",
'''

tokens = [
    'IDENTIFIER',
    'NEWLINE_NL',
    'TOK_SEMICOLON',
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
    'COMMENT_BLOCK'
    ] + list(keywords.values())

Whitesspace = "\\n\r \t"
Letters = "a-zA-Z$"
Digits = "0-9"
Parantheses = "\(\)\[\]\{\}"
Delimiters ="'`\".;,"
OpChar = "!#%&\*\+-<>=:\?\\^\|~"

Id_part1 = "[%s][%s%s]*_*[%s%s]*" %(Letters,Letters,Digits,Letters,Digits)
Id_part2 = "[%s][%s%s]*_*[%s]*" %(Letters,Letters,Digits,OpChar)
Id_part3 = "[%s]+" %OpChar

t_COMMENT_BLOCK = r"\/\*(\*(?!\/)|[^*])*\*\/"
t_COMMENT_LINE = r"\/\/.*"


def t_IDENTIFIER(t):
    #r"[a-zA-Z$][a-zA-Z$0-9]*_*[a-zA-Z$0-9]*|[a-zA-Z$][a-zA-Z$0-9]*_*[!#%&\*\+-/<>=:\?\^\|~]*|[!#%&\*\+-/<>=:\?\^\|~]+"
    r"[a-zA-Z$][a-zA-Z$0-9]*_*[a-zA-Z$0-9]*|[a-zA-Z$][a-zA-Z$0-9]*_*[!#%&\*\+\-<>=:\?\^\|~]*|[!#%&\*\+\-<>=:\?\^\|~]+"
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t


def t_TOK_LPAREN(t):
    r"\("
    lexer.paranthesis+=1
    return t
    
def t_TOK_RPAREN(t):
    r"\)"
    lexer.paranthesis-=1
    if (lexer.paranthesis <0):
        print("Unexpected ) at line no. %d" %(t.lineno))
    else:
        return t

def t_TOK_LSQB(t):
    r"\["
    lexer.paranthesis_square+=1
    return t
    
def t_TOK_RSQB(t):
    r"\]"
    lexer.paranthesis_square-=1
    if (lexer.paranthesis_square <0):
        print("Unexpected ] at line no. %d" %(t.lineno))
    else:
        return t

def t_TOK_LCUR(t):
    r"\{"
    lexer.paranthesis_curly += 1
    return t
    
def t_TOK_RCUR(t):
    r"\}"
    lexer.paranthesis_curly -=1
    if (lexer.paranthesis_curly <0):
        print("Unexpected } at line no. %d" %(t.lineno))
    else:
        return t


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_REMAINDER = r'%'

t_TOK_ASSIGN = r'='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='


t_TOK_COLON = r':'
t_LT_MINUS = r'<-'
t_TOK_LE_COLON = r'<:'
t_LT_PERCENT = r'<%'
t_TOK_GT_COLON = r'>:'
t_HASH = r'#'
t_TOK_AT = r'@'
t_TOK_COMMA = r','
t_TOK_UNDERSCORE = r'_'
t_TOK_DOT = r'.'



t_OR = r'\|\|'
t_AND = r'&&'
t_XOR = r'\^'
t_EQUAL = r'=='
t_NEQUAL = r'!='
t_GREATER = r'>'
t_TOK_EQ_GT = r'>='
t_LESS = r'<'
t_LEQ = r'<='

t_AND_BITWISE = r'&'
t_OR_BITWISE = r'\|'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_TILDA = r'\~'


t_NEWLINE_NL = r'[\n]'
t_TOK_SEMICOLON = r'[;]'

t_INTEGER_LITS = r"-[%s]+[lL]?|[%s]+[lL]?" %(Digits,Digits)
t_F_POINT_LITS = r'[0-9]*\.[0-9]+[Ee][+-][0-9]+[fFdD]?|[0-9]*\.[0-9]+'

t_BOOLEAN_LITS = r'\'true\'|\'false\''

t_CHAR_LITS = r'\'[\w\s]\''

t_STR_LITS = r'"[^"\n]+"'

t_WSPACE_LIT = r'[ \t]'


t_SQUOTES = r'\''

t_DQUOTES = r'"'

#t_COMMENTS=  r"[ ]*\{[^\n]*\}"
#t_COMMENTS=  r"[ ]*\{[^\n]*\}""


def t_newline(t):
    r"\n"
    t.lexer.lineno+=1


# Error Handling rule
def t_error(t):
    print("Illegal Character '%s' at Line No. %s" % (t.value[0], t.lineno ) )
    t.lexer.skip(1)


lexer = lex.lex()
lexer.paranthesis = 0
lexer.paranthesis_square = 0
lexer.paranthesis_curly = 0
lexer.lines = 0

filename = sys.argv[1]

# Print function defined in test.py
l1 = Print(lexer,filename)
