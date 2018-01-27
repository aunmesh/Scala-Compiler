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
    'NEWLINE CHARACTERS',
    'LITERALS',
    'INTEGER_LITERALS',
    'FLOARINGG_POINT_LITERALS',
    'BOOLEAN_LITERALS',
    'CHARACTER_LITERALS',
    'STRING_LITERALS',
    'ESCAPE_SEQUENCES',
    'WHTIESPACE_AND_COMMENTS',
    'TRAILING_COMMAS'  
]

'''
Hexdigit = ‘[0-9A-Fa-F]’
Unicode = ‘\\u+’ + Hexdigit + Hexdigit + Hexdigit + Hexdigit
Whitesspace = ‘[\\n\r \t]’
Letters = ‘[a-zA-Z$_]’
Digits = ‘[0-9]’
Parantheses = ‘[\(\)\[\]\{\}]’
Delimiters = ‘[\’`”.;,]’
OpChar = ‘[!#%&\*\+-/<>=:\?\\^\|~]’
'''

'''
There are three ways to form an identifier. First, an identifier can start with a 
letter which can be followed by an arbitrary sequence of letters and digits. This 
may be followed by underscore ‘_‘ characters and another string composed of either 
letters and digits or of operator characters. 

Second, an identifier can start with an
operator character followed by an arbitrary sequence of operator characters. The 
preceding two forms are called plain identifiers.

Finally, an identifier may also be
formed by an arbitrary string between back-quotes (host systems may impose some 
restrictions on which strings are legal for identifiers). The identifier then is 
composed of all characters excluding the backquotes themselves.


op       ::=  opchar {opchar}
varid    ::=  lower idrest
boundvarid ::=  varid
             | ‘`’ varid ‘`’
plainid  ::=  upper idrest
           |  varid
           |  op
id       ::=  plainid
           |  ‘`’ { charNoBackQuoteOrNewline | UnicodeEscape | charEscapeSeq } ‘`’
idrest   ::=  {letter | digit} [‘_’ op]
'''


Hexdigit = ‘0-9A-Fa-F’
Unicode = ‘\\u+’ + Hexdigit + Hexdigit + Hexdigit + Hexdigit
Whitesspace = ‘\\n\r \t’
Letters = ‘a-zA-Z$_’
Digits = ‘0-9’
Parantheses = ‘\(\)\[\]\{\}’
Delimiters = ‘\’`”.;,’
OpChar = ‘!#%&\*\+-/<>=:\?\\^\|~’

Op = OpChar + '+'

t_IDENTIFIER = r'[%s][%s%s]*_*[[%s%s]*[%s]]' %Letters %Letters %Digits %Letters %Digits %OpChar


'''
#Regular expression for identifiers
def t_IDENTIFIER(t):
    #r'[a-zA-Z][a-zA-Z0-9]*_*[[a-zA-Z0-9]*[!#%&\*\+-/<>=:\?\\^\|~]]'
    r'[%s][%s%s]*_*[[%s%s]*[%s]]' %Letters %Letters %Digits %Letters %Digits %OpChar
'''

