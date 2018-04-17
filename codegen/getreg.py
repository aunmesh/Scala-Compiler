import main
def init_reg():
	for i in range(0,10):
		main.rd['$t' + str(i)] = []
		main.regline['$t' + str(i)] = 0

def rd_add(reg,var):					#only adds reg into address descr. of var and var into reg descr. of reg
	if var not in main.rd[reg]:
		main.rd[reg].append(var)
		main.ad[var].append(reg)

def rd_del(var):						#Clears register fields of a variable
	for reg in main.ad[var]:
		main.rd[reg].remove(var)
		main.ad[var].remove(reg)

def rd_remove(reg,var):
	if reg in main.ad[var]:
		main.rd[reg].remove(var)
		main.ad[var].remove(reg)


def spill(reg):
	for var in main.rd[reg]:
		main.ad[var].remove(reg)
		if len(main.ad[var]) == 0 and var not in main.mem:
			print "\t" + "sw " + reg + ", " + var
			main.mem.append(var)
	main.rd[reg] = []

def clearmem(var):
	if var in main.mem:
		main.mem.remove(var)

def check_reg(var,line):
	if len(main.ad[var]) == 0:
		return find_reg(line), -1
	else:
		return main.ad[var][0], 1 

def find_reg(line):
	for reg in main.rd:
		if main.regline[reg] != line and len(main.rd[reg]) == 0:
			main.regline[reg] = line
			return reg
	
	temp = 100000
	if len(main.live[line]) == 0:
		for reg in main.rd:  
			if main.regline[reg] != line and len(main.rd[reg]) < temp:
				temp = len(main.rd[reg])
				ind = reg		 
	else:
		for var in main.live[line]:
			for reg in main.ad[var]:  
				if main.regline[reg] != line and len(main.rd[reg]) < temp:
					temp = len(main.rd[reg])
					ind = reg
			if temp != 100000:
				break
	reg = ind 
	spill(reg)
	main.regline[reg] = line
	return reg

def get_regx(x, y, line):

	if len(main.ad[y]) > 1:
		for reg in main.ad[y]:
			if main.regline[reg] == line:
				continue
			flag=1
			for var in main.rd[reg]:
				if len(main.ad[var]) == 1:
					flag = 0
			if flag == 1:
				rd_remove(reg,y)
				main.regline[reg] = line
				return reg

	if len(main.ad[y]) == 1:
		if y not in main.live[line]:
			reg = main.ad[y][0]
			if main.regline[reg] != line:
				flag = 1
				for var in main.rd[reg]:
					if len(main.ad[var]) == 1:
						flag = 0
				if flag == 1:
					rd_remove(reg,y)
					main.regline[reg] = line
					return reg

	return find_reg(line)

def get_reg(x,y,z,line):
	regx = get_regx(x, y, line)

	for reg in main.ad[z]:
		if main.regline[reg] != line:
			regz = reg
			main.regline[reg] = line
			return regx, regz

	regz = find_reg(line)
	return regx,regz

def update_dead(var,line):
	#print "var =" + var
	#print "line =" + str(line)
	if var not in main.live[line] and (var in main.ad) and len(main.ad[var]) >0:
		if var not in main.mem:
			print "\t" + "sw " + main.ad[var][0] + ", " + var
			main.mem.append(var)
		for reg in main.ad[var]:
			main.rd[reg].remove(var)
			main.ad[var].remove(reg)
