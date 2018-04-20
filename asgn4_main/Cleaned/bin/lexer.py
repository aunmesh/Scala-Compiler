# -*- coding: utf-8 -*-

from ply import lex as lex
import re,sys
#from test import *

keywords = {
    'abstract' : 'KW_abstract',
    'Array': 'KW_array',
    'by' : 'KW_by',
    'Boolean' : 'KW_boolean',
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
    'null' : 'KW_null',
    'object' : 'KW_obj',
    'ofDim' : 'KW_ofdim',
    'or' : 'KW_or',
    'override' : 'KW_override',
    'package' : 'KW_package',
    'private' : 'KW_private',
    'protected' : 'KW_protected',
    'return' : 'KW_return',
    'sealed' : 'KW_sealed',
    'super' : 'KW_super',
    'this' : 'KW_this',
    'throw' : 'KW_throw',
    'to' : 'KW_to',
    'trait' : 'KW_trait',
    'Try' : 'KW_Try',
    'true' : 'KW_true',
    'type' : 'KW_type',
    'until': 'KW_until',
    'val' : 'KW_val',
    'var' : 'KW_var',
    'while' : 'KW_while',
    'with' : 'KW_with',
    'yield' : 'KW_yield',
    'Double' : 'KW_double',
    'Int' : 'KW_int',
    'Char' : 'KW_char',
    'String' : 'KW_string',
    'Unit' : 'KW_void',
}

tokens = [
	'TOK_colon',
	'TOK_addassign',
	'TOK_mulassign',
	'TOK_divassign',
	'TOK_modassign',
    'TOK_subassign',
	'TOK_equal',
	'TOK_nequal',
	'TOK_lshift',
	'TOK_rshift',
	'TOK_geq',
	'TOK_leq',
	'TOK_greater',
	'TOK_lesser',
	'TOK_assignment',
	'TOK_plus',
	'TOK_minus',
	'TOK_times',
	'TOK_divide',
	'TOK_modulus',
	'TOK_tilda',
	'TOK_not',
	'TOK_eq_gt',
	'TOK_choose',
	'TOK_at',
	'TOK_comma',
	'TOK_hash',
	'TOK_or',
	'TOK_and',
	'TOK_or_bitwise',
	'TOK_and_bitwise',
	'TOK_xor',
	'TOK_dot',
	'TOK_identifier',
	'TOK_paraleft',
	'TOK_pararight',
	'TOK_lsqb',
	'TOK_rsqb',
	'TOK_lcurly',
	'TOK_rcurly',
	'TOK_string',
	'TOK_char',
	'TOK_nl',
	'TOK_semi',
	'TOK_int',
	'TOK_long',
	'TOK_float',
	'TOK_ignore',
	'TOK_cmnt',
	'TOK_error'
] + list(keywords.values())

t_TOK_colon = r':'
t_TOK_addassign = r'\+='
t_TOK_mulassign = r'\*='
t_TOK_divassign = r'='
t_TOK_subassign = r'-='
t_TOK_modassign = r'%='
t_TOK_equal = r'=='
t_TOK_nequal = r'!='
t_TOK_lshift = r'<<'
t_TOK_rshift = r'>>'
t_TOK_geq = r'>='
t_TOK_leq = r'<='
t_TOK_greater = r'>'
t_TOK_lesser = r'<'
t_TOK_assignment = r'='
t_TOK_plus = r'\+'
t_TOK_minus = r'-'
t_TOK_times = r'\*'
t_TOK_divide = r'/'
t_TOK_modulus = r'%'
t_TOK_tilda = r'~'
t_TOK_not = '!'
t_TOK_eq_gt = '=>'
t_TOK_choose = '<-'
t_TOK_at = r'@'
t_TOK_comma = r','
t_TOK_hash = r'\#'
t_TOK_or = r'\|\|'
t_TOK_and = r'&&'
t_TOK_or_bitwise = r'\|'
t_TOK_and_bitwise = r'\&'
t_TOK_xor = r'\^'
t_TOK_dot = r'\.'

def t_TOK_identifier(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = keywords.get(t.value, 'TOK_identifier')
    return t

def t_TOK_paraleft(t):
    r"\("
    lexer.paranthesis+=1
    return t
    
def t_TOK_pararight(t):
    r"\)"
    lexer.paranthesis-=1
    if (lexer.paranthesis <0):
        print("Unexpected ) at line no. %d" %(t.lineno))
    else:
        return t

def t_TOK_lsqb(t):
    r"\["
    lexer.paranthesis_square+=1
    return t
    
def t_TOK_rsqb(t):
    r"\]"
    lexer.paranthesis_square-=1
    if (lexer.paranthesis_square <0):
        print("Unexpected ] at line no. %d" %(t.lineno))
    else:
        return t

def t_TOK_lcurly(t):
    r"\{"
    lexer.paranthesis_curly += 1
    return t
    
def t_TOK_rcurly(t):
    r"\}"
    lexer.paranthesis_curly -=1
    if (lexer.paranthesis_curly <0):
        print("Unexpected } at line no. %d" %(t.lineno))
    else:
        return t

#t_BOOLEAN_LITS = r'\'true\'|\'false\''

def t_TOK_string(t):
    r'"[^"\n]*"'
    t.value=t.value[1:-1]
    return t

def t_TOK_char(t):
    r'\'.\''
    t.value = t.value[1:-1]
    return t


def t_TOK_nl(t):
    r"\n"
    t.lexer.lineno+=1

def t_TOK_semi(t):
    r";"
    return t

def t_TOK_int(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t

def t_TOK_long(t):
    r'[-+]?\d+(L|l)'
    t.value = int(t.value)
    return t

def t_TOK_float(t):
    r'((\d+)(\.\d+)([eE](\+|-)?(\d+))? | (\d+)[eE](\+|-)?(\d+))([lL]|[fF])?'
    t.value = float(t.value)
    return t

t_ignore  = ' \t'

def t_TOK_cmnt(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


# Error Handling rule
def t_error(t):
    print("Illegal Character '%s' at Line No. %s" % (t.value[0], t.lineno ) )
    t.lexer.skip(1)


lexer = lex.lex()
lexer.paranthesis = 0
lexer.paranthesis_square = 0
lexer.paranthesis_curly = 0
lexer.lines = 0

#filename = sys.argv[1]

# Print function defined in test.py
#l1 = Print(lexer,filename)