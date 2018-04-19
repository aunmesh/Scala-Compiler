import ply.lex as lex

# List of token names.   This is always required

reserved = {
'if' 		: 'KEYWORD_IF',
'else' 		: 'KEYWORD_ELSE',
'for' 		: 'KEYWORD_FOR',
'while' 	: 'KEYWORD_WHILE',
'do' 		: 'KEYWORD_DO',
'var' 		: 'KEYWORD_VAR',
'val' 		: 'KEYWORD_VAL',
'return' 	: 'KEYWORD_RETURN',
'type' 		: 'KEYWORD_TYPE',
'define'	: 'KEYWORD_DEFINE',
'object' 	: 'KEYWORD_OBJECT',
'case' 		: 'KEYWORD_CASE',
'def' 		: 'KEYWORD_DEF',
'new' 		: 'KEYWORD_NEW',
'by'        : 'KEYWORD_BY',
'until'     : 'KEYWORD_UNTIL',
'to'        : 'KEYWORD_TO',
'true'      : 'BOOL_CONSTT',
'false'     : 'BOOL_CONSTF',
'match'     : 'KEYWORD_MATCH',
'Array'		: 'KEYWORD_ARRAY',
'print'		: 'KEYWORD_PRINT',
'println'	: 'KEYWORD_PRINTLN',
'scan'		: 'KEYWORD_SCAN',
'Int'		: 'TYPE_INT',
'Long'		: 'TYPE_INT',
'String'	: 'TYPE_STRING',
'Float'		: 'TYPE_DOUBLE',
'Double'	: 'TYPE_DOUBLE',
'Char'		: 'TYPE_CHAR',
'Boolean'	: 'TYPE_BOOLEAN',
'Unit'      : 'TYPE_VOID'
}


def t_DOUBLE_NUMBER(t):
	r'\b[-+]?[0-9]*\.[0-9]*([eE][-+]?[0-9]+)?([FfDd])?\b| \b[-+]?[0-9]*([eE][-+]?[0-9]+)([FfDd])?\b | [-+]?\d+[FfdD]\b'
	if(t.value == '.'):
		 t.type = 'INST'
		 return t
	if (t.value[-1]=='F' or t.value[-1]=='f' or t.value[-1]=='D' or t.value[-1]=='d'):
		t.value=t.value[:-1]
	t.value = float(t.value)    
	return t

def t_INT_NUMBER(t):
	r'[-+]?\d+([lL])?\b'
	if (t.value[-1]=='l' or t.value[-1]=='L'):
		t.value=t.value[:-1]
	t.value = int(t.value)    
	return t

tokens = [
	'LPAREN', 'RPAREN',
	'BLOCKBEGIN','BLOCKEND',
	'LBRAC','RBRAC',
	'INT_NUMBER','DOUBLE_NUMBER',
	'COLON','COMMA','TERMINATOR','INST',
	'PLUS', 'MINUS','TIMES','DIVIDE','REMAINDER',
	'GREATER','LESS','GEQ','LEQ','EQUAL','NEQUAL',
	'OR_BITWISE','AND_BITWISE','TILDA','LSHIFT','RSHIFT','XOR',
	'AND','OR','NOT',
	'ASOP','TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'REMAINDER_ASSIGN',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'LSHIFT_ASSIGN',
    'RSHIFT_ASSIGN',
    'AND_ASSIGN',
    'OR_ASSIGN',
    'XOR_ASSIGN',
	'IDENTIFIER',
	'COMMENT','COMMENT_BEGIN','COMMENT_END',
	'STRING','CHAR','FUNTYPE','CHOOSE'
] + list(reserved.values())


# Regular expression rules for simple tokens
t_PLUS       = r'\+'
t_MINUS 	 = r'-'
t_TIMES 	 = r'\*'
t_DIVIDE 	 = r'/'
t_REMAINDER  = r'%'

t_ASOP 	 	 = r'='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_REMAINDER_ASSIGN = r'%='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='

t_LPAREN     = r'\('
t_RPAREN     = r'\)'

t_BLOCKBEGIN = r'\{'
t_BLOCKEND   = r'\}'

t_LBRAC   	 = r'\['
t_RBRAC      = r'\]'

t_COLON      = r'\:'
t_COMMA      = r'\,'
t_TERMINATOR = r'\;'
t_INST     	 = r'\.'
t_FUNTYPE    = r'=>'
t_CHOOSE     = r'<-'

t_EQUAL 	 = r'=='
t_NEQUAL 	 = r'!='
t_GREATER 	 = r'>'
t_GEQ 		 = r'>='
t_LESS 		 = r'<'
t_LEQ 		 = r'<='

t_AND_BITWISE = r'&'
t_OR_BITWISE  = r'\|'
t_XOR		  = r'\^'
t_LSHIFT	  = r'<<'
t_RSHIFT	  = r'>>'
t_TILDA		  = r'\~'

t_AND 		  = r'&&'
t_OR 		  = r'\|\|'
t_NOT 		  = r'!'

def t_STRING(t):
	r'"[^"\n]*"'
	t.value=t.value[1:-1]
	return t

def t_CHAR(t):
	r'\'.\''
	t.value=t.value[1:-1]
	return t

def t_IDENTIFIER(t):
	r'\b[_a-zA-Z][_a-zA-Z0-9]*'
	t.type = reserved.get(t.value,'IDENTIFIER')
	return t


# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_COMMENT(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
	pass

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
# Build the lexer
lexer = lex.lex()