import main
import livegen
import getreg
import sys
import cPickle as pickle

def NAME(op):
	if( op == '+'):
		return "add"
	elif(op == '-'):
		return "sub"
	elif (op == '/' or op == '%'):
		return "div"
	elif(op == '*'):
		return "mult"
	elif (op == '^'):
		return "xor"
	elif (op == '|'):
		return "or"
	elif (op == '&'):
		return "and"
	elif (op == "<="):
		return "ble"
	elif (op == ">="):
		return "bge"
	elif (op == "=="):
		return "beq"
	elif (op == "!="):
		return "bne"
	elif (op == ">"):
		return "bgt"
	elif (op == "<"):
		return "blt"


def MOVE(reg,y):                    # Load the variable value contained in y to reg
	if len(main.ad[y])==0 and y != 'return':
		print "\t" + "lw " + reg + ", " + getmem(y)
	elif (reg!= main.ad[y][0]):
			print "\t" + "move " + reg + ", " + main.ad[y][0] 



def VOP(op,regz,regx):
	if(op in ['mult', 'div']):
		print "\t" + op + " " + regx + ', ' + regz
	else:
		print "\t" + op + " " + regx + ', ' + regx + ', ' + regz

def COP(op,z,reg):                  # here value(reg) = value(reg) op int(z)
	print "\t" + "li $a0," + z
	if(op in ['mult', 'div']):
		print "\t" + op + " " + reg + ', $a0'
	else:
		print "\t" + op + " " + reg + ', ' + reg + ', $a0'


def UPDATE(x,reg):
	getreg.mem_clear(x)
	getreg.rd_del(x)
	getreg.rd_add(reg,x)

def LOADADDR(y, reg):
	if y not in variable_list:
		print "\t" + "la " + reg +", " + y
	else:
		y = getmem(y)
		print "\t" + "add " + reg + ", $fp " + y[:-5]


def XequalY(x,y):
	if(y.isdigit()):
				reg = getreg.find_reg(lno)
				print "\t" + "li " + reg + ", " + y
				UPDATE(x,reg)
	else:       
				if y in main.map_ptr:
					main.map_ptr[x] = main.map_ptr[y]
					getreg.rd_del(x)
					getreg.mem_clear(x)
				else:
					if x in main.map_ptr:
						del main.map_ptr[x]

					if y != 'return':
						reg = getreg.regx_get(x,y,lno)
					else:
						reg = getreg.find_reg(lno)
	
					MOVE(reg,y)
					UPDATE(x,reg)

identifiers = {}
arrays = {}


filename = sys.argv[1]
main.testfile = sys.argv[1] + '.ir'
livegen.gen_live()
getreg.init_reg()
print "\t" + ".data"

lines = open(main.testfile,"r").readlines()


for line in lines:
	line = line.split()
	if line[1] in ['+','-','/','*','%','&','|','^', ">>" , "<<"]:
		if line[2] not in identifiers:
			identifiers[line[2]]=1
	elif line[1]=='=':
		if('[' not in line and '&' not in line and '*' not in line):
			if line[2] not in identifiers:
				identifiers[line[2]]=1
		elif line[-1]==']':
			if line[2] not in identifiers:
				identifiers[line[2]]=1
		elif line[2] == '*':
			if line[3] not in identifiers:
				identifiers[line[3]]=1
		elif line[3] in ['&','*'] :
			if line[2] not in identifiers:
				identifiers[line[2]]=1

	if line[1]=="=s":
			print line[2] + ":\t.asciiz " +  " ".join(line[3:])
	
	elif line[1]== 'Array':
		if line[2] not in arrays:
			arrays[line[2]] = line[3]

variable_list = pickle.load(open(filename + '_var_list.p', 'rb'))

# print variable_list

for identifier in identifiers:
	if identifier not in arrays:
		if identifiers[identifier] == 1:
			if identifier not in variable_list:
				print identifier + ":\t.word\t0"
				main.memad[identifier] = identifier
			main.ad[identifier] = []

for array in arrays:
	if array not in variable_list:
		main.memad[array] = array
		print array + ":\t.space\t" + arrays[array]

print "\n"

print "\t" + ".text"
#print "main:"


function_list = pickle.load(open(filename + '_func_list.p', 'rb'))

# print function_list

for i in function_list:
	fun = function_list[i]
	size = 0
	for variable in fun['local']:
		if fun['local'][variable]['type'] == 'array':
			size -= 4 * int(fun['local'][variable]['size'])
		else:
			size -= 4
		main.memad[variable] = str(size) + '($fp)'

	for temp in function_list[i]['temp']:
		size -= 4
		main.memad[temp] = str(size) + '($fp)'
	
	size = 12 + (len(fun['param'])-1)*4

	for i in range(1,len(fun['param']) + 1):
		main.memad[fun['param'][i]['place']] = str(size) + '($fp)'
		size -= 4

main.memad['return'] = '$v0'
main.ad['return'] = ['$v0']

def getmem(x):
	return main.memad[x]


for line in lines:
	line = line.split()
	if len(line) == 0:
		break
	lno = int(line[0])
	# print lno
	op = line[1]
	if main.block_get[lno] != main.block_get[lno-1]:
		print "\nBLOCK" + str(main.block_get[lno]) + ":"
	if (op == '='):
		if('[' not in line and '&' not in line and '*' not in line):            # x = y
			x = line[2]
			y = line[3]
			XequalY(x,y)
		elif '[' in line:                 # x[i] = y or x = y[i]
			if( line[-1] == ']'):            # x = y[i]
				x = line[-5]
				y = line[-4] 
				i = line[-2]
				reg = getreg.regx_get(x,y, lno)
				LOADADDR(y, reg)                              ##
				if(i.isdigit()): 
					print "\t" + "addi " + reg + ', ' + str(4*int(i))
				else:
					MOVE('$a0',i)
					print "\t" +"li $a1, 4"
					print "\t" +"mult $a0, $a1"
					print "\t" +"mflo $a0"
					print "\t" +"add " + reg + ' , ' + reg + ", $a0" 
				print "\t" +"lw " + reg + ", 0(" + reg + ')'
				UPDATE(x,reg)
			else:
				x = line[2]                            # x[i] = y
				y = line[6]
				i = line[4]
				reg = getreg.regx_get(x,y,lno)
				LOADADDR(x,reg)
				if(i.isdigit()): 
					print "\t" + "addi " + reg + ', ' + str(4*int(i))
				else:
					MOVE('$a0',i)
					print "\t" + "li $a1, 4"
					print "\t" + " mult $a0, $a1"
					print "\t" + "mflo $a0"
					print "\t" + "add " + reg + ' , ' + reg + ", $a0" 
				if(y.isdigit()):
					print "\t" + "li $a0, " + y
				else:
					MOVE('$a0',y)
				print "\t" + "sw $a0, 0(" + reg + ')'
		elif('&' in line):        # = x & y
			x = line[2]
			y = line[4]
			main.map_ptr[x] = y
			getreg.rd_del(x)
			getreg.mem_clear(x)
		elif("*" in line):        # = * x y      or = x * y
			if(line[2] == '*'):
				x = line[3]
				y = line[4]
				z = main.map_ptr[x]
				XequalY(z,y)
			else:
				x = line[2]
				y = line[4]
				z = main.map_ptr[y]
				XequalY(x,z)



	elif (op in ['+','-','*','/','%','|','^','&','<<','>>']):           # x = y op z  where x & y are variables and z can or cannot be
		x = line[2]
		y = line[3]
		z = line[4]

		
		if(z.isdigit() and y.isdigit()):
				reg = getreg.find_reg(lno)
				if(op == '+'):
					val = int(y) + int(z)
				elif(op == '-'):
					val = int(y) - int(z)
				elif(op == '/'):
					val = int(y) / int(z)
				elif(op == '*'):
					val = int(y) * int(z)
				elif(op == '%'):
					val = int(y) % int(z)
				elif(op == '^'):
					val = int(y) ^ int(z)
				elif(op == '<<'):
					val = int(y) << int(z)
				elif(op == '>>'):
					val = int(y) >> int(z)

				print "\t" +"li " + reg +", " + str(val)
				UPDATE(x,reg)
		
		#	else:
			#if(y.isdigit()):    # + - /
			#	tmp = y
			#	y = z
			#	z= temp

		else:
			if(z.isdigit()):
				regz = getreg.find_reg(lno)
				print "\t" +"li " + regz +", " + str(z)	
				reg = getreg.regx_get(x,y,lno)
				MOVE(reg,y)
				if (op in ['+','-','*','/','%','|','^','&']):
					VOP(NAME(op), regz, reg)
				elif( op == '>>'):
					VOP('srl', regz, reg)
				elif (op == '<<'):
					VOP('sll', regz, reg)
				UPDATE(x,reg)
			elif(y.isdigit()):
				reg = getreg.find_reg(lno)
				print "\t" +"li " + reg +", " + str(y)
				regz = getreg.regx_get(x,z,lno)
				MOVE(regz,z)
				if (op in ['+','-','*','/','%','|','^','&']):
					VOP(NAME(op), regz, reg)
				elif( op == '>>'):
					VOP('srl', regz, reg)
				elif (op == '<<'):
					VOP('sll', regz, reg)
				UPDATE(x,reg)
			else:
				(reg,regz) = getreg.reg_get(x,y,z,lno)
				MOVE(reg,y)
				MOVE(regz,z)
				if (op in ['+','-','*','/','%','|','^','&']):
					VOP(NAME(op), regz, reg)
				elif (op == '<<'):
					VOP('sll', regz, reg)
				elif( op == '>>'):
					VOP('srl', regz, reg)

				UPDATE(x,reg)
				UPDATE(z,regz)
			if(op == '*' or op =='/'):
				print "\t" + "mflo " + reg 
			elif(op =='%'):
				print "\t" + "mfhi " + reg 
			

	elif op == '~':
		x = line[2]
		y = line[3]
		reg = getreg.regx_get(x,y,lno)
		MOVE(reg,y);
		print "\t" + "li $a0, -1"
		print "\t" + "xor " + reg + ' , ' + reg + ", $a0"
		UPDATE(x,reg)
		
	elif op == "ifgoto":
		x = line[-2]
		y = line[-1]
		relop = line[-3]
		branch = int(line[2])

		if(y.isdigit()):
			(reg,state) = getreg.reg_check(x,lno)
			if(state == -1):
				print "\t" + "lw " + reg + ", " + getmem(x)
				getreg.rd_del(x)
				getreg.rd_add(reg,x)
			print "\t" + NAME(relop) + " " + reg + ", " + y + ", " + "BLOCK" + str(main.block_get[branch])
		else:
			(regx,state) = getreg.reg_check(x,lno)
			if(state == -1):
				print "\t" + "lw " + regx + ", " + getmem(x)
				getreg.rd_del(x)
				getreg.rd_add(regx,x)
			(regy,state) = getreg.reg_check(y,lno)
			if(state == -1):
				print "\t" + "lw " + regy + ", " + getmem(y)
				getreg.rd_del(y)
				getreg.rd_add(regy,y)
			print "\t" + NAME(relop) + " " + regx + ", " + regy + ", " + "BLOCK" + str(main.block_get[branch])

	elif op == "goto":
		branch = int(line[2])
		print "\t" + "b " + "BLOCK" + str(main.block_get[branch])


	elif op == 'label':  #done
		x = line[2]
		print "\t" + x + ": "
		print "\t" + "addi $sp, $sp, -12"
		print "\t" + "li $a0," + str(function_list[x]['paramsize'])
		print "\t" + "sw $a0, 8($sp)"
 		print "\t" + "sw $fp, 4($sp)"
		print "\t" + "sw $ra, 0($sp)"
		print "\t" + "addi $fp, $sp, 0 "
		print "\t" + "addi $sp, $sp, " + str(-function_list[x]['localsize'])
				
	elif op == 'param' :
		x = line[2]
		if (x.isdigit()):
			print "\t" + "addi $sp, $sp, -4"
			print "\t" + "li $a0, ", x
			print "\t" + "sw $a0, 0($sp)"
		else:
			print "\t" + "addi $sp, $sp, -4"
			print "\t" + "lw $a0," + getmem(x)
			print "\t" + "sw $a0, 0($sp)"







	elif op == 'ret':
		if(len(line) > 2):                # value returning function
			x = line[2]
			if(x.isdigit()):
				print "\t" + "li $v0, " + x         #might need to store it in stack
			else:
				MOVE('$v0',x)
		print "\t" + "lw $ra, 0($fp)"
		print "\t" + "lw $a0, 8($fp)"
		print "\t" + "addi $a0, 12"
		print "\t" + "add $sp, $fp, $a0"
		print "\t" + "lw $fp, 4($fp)"
		print "\t" + "jr $ra"

 	elif op == 'call':
 	 	x = line[2]          # x contains the function name
 	 	print "\t" + "jal " + x
 	 	if(len(line)>3):     #value returning function
 	 		y = line[3]
 	 		reg = getreg.find_reg(lno)
			print "\t" + "addi " + reg + ", $v0, 0" 
			UPDATE(y,reg)

	elif ( op == 'scan'):
		x = line[2]
		reg = getreg.find_reg(lno)
		print "\t" + "li $v0, 5\n" + "\t" + "syscall"
		print "\t" + "move " + reg + ", $v0"
		UPDATE(x,reg)

	elif op == 'print':
		x = line[2]
		if (x == 'newline'):
			print "\t" + "addi $a0, $0, 0xA" 
			print "\t" + "addi $v0, $0, 0xB" 
			print "\t" + "syscall"
		else:
			if x not in identifiers:
				print "\t" + "li $v0, 4"
			else:
				print "\t" + "li $v0, 1"
			if (x.isdigit()):
				print "\t" + "li $a0, " + x
			elif x in main.map_ptr:
				#print "ffoo"
				print "\t" + "la $a0, " + main.map_ptr[x]
			else:
				#print "foo"
				if x not in identifiers:
					print "\t" + "la $a0, " + x
				else:
	 				(reg,state) = getreg.reg_check(x,lno)
					if(state == -1):
						print "\t" + "lw " + reg + ", " + getmem(x)
						getreg.rd_del(x)
						getreg.rd_add(reg,x)
					print "\t" + "move $a0, " + reg
			print "\t" + "syscall"

	elif ( op == 'exit'):
		print "\t" + "li $v0, 10\n" + "\t" + "syscall"
	
	if op != 'ifgoto' and op != 'goto' and op != 'param' and op != 'call' and op != 'ret':
		for x in line:
			getreg.update_dead(x,lno)
	else:
		getreg.clear_rd()
		getreg.clear_ad()
print "\n"	

# state -1 => new register is returned && x is in memory and not register
# state 1  => x ka register