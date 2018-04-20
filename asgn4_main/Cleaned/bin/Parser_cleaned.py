#!/usr/bin/python
import lexer as LEXER
import sys
import os
import re
import ply.yacc as yacc
from  Parser_with_Grammar import *

tokens = LEXER.tokens


#ERROR
def p_error(p):
  
	flag=-1;

	print("Syntax error at '%s'" % p.value)
	print('\t Error: {}'.format(p))



parser = yacc.yacc()

fname = sys.argv[1]

f = open(fname, "r")

prog = f.read()

f.close()

root = parser.parse(prog)



