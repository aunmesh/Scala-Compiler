# -*- coding: utf-8 -*-

from ply import lex as lex
import re

#List of token names. Always required
#TOKEN NAMES IN SCALA
'''
1 Identifiers
2 Newline Characters
3 Literals
1 Integer Literals
2 Floating Point Literals
3 Boolean Literals
4 Character Literals
5 String Literals
6 Escape Sequences
7 Symbol literals
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
     '-' : 'KW_-',
     ':' : 'KW_:',
     '=' : 'KW_=',
     '=>' : 'KW_=>',
     '<-' : 'KW_<-',
     '<:' : 'KW_<:',
     '<%' : 'KW_<%',
     '>:' : 'KW_>:',
     '#' : 'KW_\#',
     '@' : "KW_@"
}


keywords = {
    'object': 'KEYWORD_OBJECT',
    'def' : 'KEYWORD_def',
}

tokens = [
    'IDENTIFIER',
    'NEWLINE',
    'INTEGER_LITERALS',
    'FLOATING_POINT_LITERALS',
    'BOOLEAN_LITERALS',
    'CHARACTER_LITERALS',
    'STRING_LITERALS',
    'WHITESPACE_LITERAL'
    ]

#[MC6(Hexdigit = "0-9A-Fa-F"
#Unicode = "\\u+" + Hexdigit + Hexdigit + Hexdigit + Hexdigit
Whitesspace = "\\n\r \t"
Letters = "a-zA-Z$_"
Digits = "0-9"
Parantheses = "\(\)\[\]\{\}"
Delimiters ="'`\".;,"
OpChar = "!#%&\*\+-/<>=:\?\\^\|~"

Op = OpChar + '+'

Id_part1 = "[%s][%s%s]*_*[[%s%s]\*[%s]\*]" %(Letters,Letters,Digits,Letters,Digits,OpChar)
Id_part2 = "[%s]+" %OpChar
#Id_part3 = ""

t_IDENTIFIER = r'%s|%s' %(Id_part1,Id_part2)

t_NEWLINE = r'[\n;]'

t_INTEGER_LITERALS = r"-[%s]+[lL]|[%s]+[lL]" %(Digits,Digits)

#Exponent_part = '[Ee][+-][0-9]+'
t_FLOATING_POINT_LITERALS = r'%s*.%s+[\[Ee\]\[+-\]\[0-9\]\+]?[fFdD]?' %(Digits,Digits)

t_BOOLEAN_LITERALS = r'true|false'

t_CHARACTER_LITERALS = r'\'[\w\s]\''

t_STRING_LITERALS = r'\'[\w\s]+\''

t_WHITESPACE_LITERAL = r' \t'

# Error Handling rule
def t_error(t):
    print("Illegal Character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()