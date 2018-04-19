import LEXER
import re
import os
import sys
from backpatch import *
import ply.yacc as yacc
import cPickle as pickle

tokens = LEXER.tokens
START = ['ProgramStructure']

parser = yacc.yacc()

#ERROR
def p_error(p):
  
	flag=-1;

	print("Syntax error at '%s'" % p.value),
	print('\t Error: {}'.format(p))

	while 1:
		tok = yacc.token()             # Get the next token
		if not tok:
			flag=1
			break
		if tok.type == 'STATE_END': 
			flag=0
			break

	if flag==0:
		yacc.errok()
		return tok
	else:
		yacc.restart()


f = open(sys.argv[1],"r")
code_full = f.read()
f.close()

node = parser.parse(code_full)
emit(['exit', '0'])

for i in range(1,len(TAC)):
	print i,
	for j in range(len(TAC[i])):
		print TAC[i][j],
	print

function_list = {} 				# gives info about parameters and local variables of function with name as per 3AC
variable_list = {}

def get_fscopename(id):
	if dict_symboltable[id].objecttype == 'function' or dict_symboltable[id].objecttype == 'global':
		return dict_symboltable[id].name
	else:
		return get_fscopename(dict_symboltable[id].pid)

for i in range(1,len(dict_symboltable) + 1):
	d = dict_symboltable[i].table
	fname = get_fscopename(i)

	if fname == 'global':
		continue

	local = {}
	param = {}
	temp = []
	localsize = 0
	paramsize = 0

	for key in d:
		if d[key]['name'] == 'return':
			continue
			
		if d[key]['type'] == 'Int' or d[key]['type'] == 'array':
			if d[key]['scopetype'] == 'local':
				dic = {}
				dic['type'] = d[key]['type']
				if dic['type'] == 'array':
					dic['size'] = d[key]['size']
					localsize += 4*d[key]['size']
				else:
					localsize += 4
				local[d[key]['place']] = dic
				variable_list[d[key]['place']] = fname
			else:
				dic = {}
				dic['type'] = d[key]['type']
				if dic['type'] == 'array':
					dic['size'] = d[key]['size']
					paramsize += 4*d[key]['size']
				else:
					paramsize += 4
				dic['place'] = d[key]['place']
				param[d[key]['paramno']] = dic
				variable_list[d[key]['place']] = fname

	for i in dict_symboltable[i].templist:
		temp.append(i)
		variable_list[i] = fname
		localsize += 4
	if fname in function_list:
		function_list[fname]['local'].update(local)
		function_list[fname]['param'].update(param)
		function_list[fname]['temp'].extend(temp)
		function_list[fname]['localsize'] += localsize
		function_list[fname]['paramsize'] += paramsize
	else:
		function_list[fname] = {}
		function_list[fname]['local'] = local
		function_list[fname]['param'] = param
		function_list[fname]['temp'] = temp
		function_list[fname]['localsize'] = localsize
		function_list[fname]['paramsize'] = paramsize

filename = sys.argv[1]

filename = filename[:-6]

# print function_list
# print variable_list

pickle.dump(function_list, open(filename + '_func_list.p', 'wb'))
pickle.dump(variable_list, open(filename + '_var_list.p', 'wb'))