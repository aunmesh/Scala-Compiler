# -*- coding: utf-8 -*-

from ply import lex as lex
import re

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
    'abstract' : 'KW_abstract',
    'case' : 'KW_case',	
     'catch' : 'KW_catch',
     'class' : 'KW_class',
     'def' : 'KW_def',
     'do' : 'KW_do',
     'else' : 'KW_else',
     'extends' : 'KW_extends',
     'false' : 'KW_false',
     'final' : 'KW_final',
     'finally' : 'KW_finally',
     'for' : 'KW_for',
     'forSome' : 'KW_forSome',
     'if' : 'KW_if',
     'implicit' : 'KW_implicit',
     'import' : 'KW_import',
     'lazy' : 'KW_lazy',
     'match' : 'KW_match',
     'new' : 'KW_new',
     'NULL' : 'KW_NULL',
     'object' : 'KW_object',
     'override' : 'KW_override',
     'package' : 'KW_package',
     'private' : 'KW_private',
     'protected' : 'KW_protected',
     'return' : 'KW_return',
     'sealed' : 'KW_sealed',
     'super' : 'KW_super',
     'this' : 'KW_this',
     'throw' : 'KW_throw',
     'trait' : 'KW_trait',
     'Try' : 'KW_Try',
     'true' : 'KW_true',
     'type' : 'KW_type',
     'val' : 'KW_val',
     'Var' : 'KW_Var',
     'while' : 'KW_while',
     'with' : 'KW_with',
     'yield' : 'KW_yield',
     '-' : 'KW_MINUS',
     ':' : 'KW_COLON',
     '=' : 'KW_EQ',
     '=>' : 'KW_EQ_GT',
     '<-' : 'KW_LT_MINUS',
     '<:' : 'KW_LE_COLON',
     '<%' : 'KW_LT_PERCENT',
     '>:' : 'KW_GT_COLON',
     '#' : 'KW_HASH',
     '@' : "KW_AT",
     ',' : "KW_COMMA"
}

tokens = [
    'IDENTIFIER',
    'NEWLINE',
    'INTEGER_LITS',
    'F_POINT_LITS',
    'BOOLEAN_LITS',
    'CHAR_LITS',
    'STR_LITS',
    'WSPACE_LIT',
    'PARALEFT',
    'PARARIGHT',
    'PARALSQUARE',
    'PARARSQUARE',
    'PARALCURLY',
    'PARARCURLY',
    'SQUOTES',
    'DQUOTES'
    ] + list(keywords.values())

#[MC6(Hexdigit = "0-9A-Fa-F"
#Unicode = "\\u+" + Hexdigit + Hexdigit + Hexdigit + Hexdigit

Whitesspace = "\\n\r \t"
Letters = "a-zA-Z$"
Digits = "0-9"
Parantheses = "\(\)\[\]\{\}"
Delimiters ="'`\".;,"
OpChar = "!#%&\*\+-/<>=:\?\\^\|~"

#Id_part1 = "[%s][%s%s]*_*[[%s%s]\*[%s]\*]" %(Letters,Letters,Digits,Letters,Digits,OpChar)
Id_part1 = "[%s][%s%s]*_*[%s%s]*" %(Letters,Letters,Digits,Letters,Digits)
Id_part2 = "[%s][%s%s]*_*[%s]*" %(Letters,Letters,Digits,OpChar)
Id_part3 = "[%s]+" %OpChar
#Id_part4 = ""

#t_IDENTIFIER = r'%s|%s|%s' %(Id_part1,Id_part2, Id_part3)


def t_IDENTIFIER(t):
    r"[a-zA-Z$][a-zA-Z$0-9]*_*[a-zA-Z$0-9]*|[a-zA-Z$][a-zA-Z$0-9]*_*[!#%&\*\+-/<>=:\?\^\|~]*|[!#%&\*\+-/<>=:\?\^\|~]+"
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t





def t_PARALEFT(t):
    r"\("
    lexer.paranthesis+=1
    return t
    
def t_PARARIGHT(t):
    r"\)"
    lexer.paranthesis-=1
    if (lexer.paranthesis <0):
        print("Unexpected ) at line no. %d" %(t.lineno))
    else:
        return t


def t_PARALSQUARE(t):
    r"\["
    lexer.paranthesis_square+=1
    return t
    
def t_PARARSQUARE(t):
    r"\]"
    lexer.paranthesis_square-=1
    if (lexer.paranthesis_square <0):
        print("Unexpected ] at line no. %d" %(t.lineno))
    else:
        return t



def t_PARALCURLY(t):
    r"\{"
    lexer.paranthesis_curly += 1
    return t
    
def t_PARARCURLY(t):
    r"\}"
    lexer.paranthesis_curly -=1
    if (lexer.paranthesis_curly <0):
        print("Unexpected } at line no. %d" %(t.lineno))
    else:
        return t



#print t_IDENTIFIER
t_NEWLINE = r'[\n;]'

t_INTEGER_LITS = r"-[%s]+[lL]?|[%s]+[lL]?" %(Digits,Digits)
print t_INTEGER_LITS

#Exponent_part = '[Ee][+-][0-9]+'
t_F_POINT_LITS = r'%s*.%s+[\[Ee\]\[+-\]\[0-9\]\+]?[fFdD]?' %(Digits,Digits)

t_BOOLEAN_LITS = r'true|false'

t_CHAR_LITS = r'\'[\w\s]\''

t_STR_LITS = r'\'[\w\s]+\''

t_WSPACE_LIT = r'[ \t]'

t_SQUOTES = r'\''

t_DQUOTES = r'"'

# Error Handling rule
def t_error(t):
    print("Illegal Character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.paranthesis = 0
lexer.paranthesis_square = 0
lexer.paranthesis_curly = 0

l1 = Print(lexer,'Scala.txt')





