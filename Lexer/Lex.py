# -*- coding: utf-8 -*-

from ply import lex as lex
import re

'''
 object HelloWorld {
    def main(args: Array[String]) {
      println("Hello, world!")
    }
  }
'''

#List of token names. Always required

#Reserved words in Scala (not to be included in identifiers)
'''
abstract	case	catch	class
def	do	else	extends
false	final	finally	for
forSome	if	implicit	import
lazy	match	new	Null
object	override	package	private
protected	return	sealed	super
this	throw	trait	Try
true	type	val	Var
while	with	yield	 
-	:	=	=>
<-	<:	<%	>:
#	@
'''

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

#Hexdigit = [0-9A-Fa-F]
#Unicode = \\u+ + Hexdigit + Hexdigit + Hexdigit + HexdigitWhitesspace = \\n\r \t
#Letters = a-zA-Z$_
#Digits = 0-9
#Parantheses = \(\)\[\]\{\}
#Delimiters = \’`”.;,
#OpChar = !#%&\*\+-/<>=:\?\\^\|~

Hexdigit = "0-9A-Fa-F"
Unicode = "\\u+" + Hexdigit + Hexdigit + Hexdigit + Hexdigit
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
print t_IDENTIFIER

t_NEWLINE = r'[\n;]'

t_INTEGER_LITERALS = r"-[%s]+[lL]|[%s]+[lL]" %(Digits,Digits)

#Exponent_part = '[Ee][+-][0-9]+'
t_FLOATING_POINT_LITERALS = r'%s*.%s+[\[Ee\]\[+-\]\[0-9\]\+]?[fFdD]?' %(Digits,Digits)

t_BOOLEAN_LITERALS = r'true|false'

t_CHARACTER_LITERALS = r'\'[\w\s]\''

t_STRING_LITERALS = r'\'[\w\s]+\''

t_WHITESPACE_LITERAL = r' \t'

lexer = lex.lex()
#r"-[%s].[%s]"




'''
#Regular expression for identifiers
def t_IDENTIFIER(t):
    #r'[a-zA-Z][a-zA-Z0-9]*_*[[a-zA-Z0-9]*[!#%&\*\+-/<>=:\?\\^\|~]]'
    r'[%s][%s%s]*_*[[%s%s]*[%s]]' %Letters %Letters %Digits %Letters %Digits %OpChar
'''

