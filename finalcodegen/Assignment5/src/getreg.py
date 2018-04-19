import main

def init_reg():
	for i in range(0,10):
		main.rd['$t' + str(i)] = []
		main.regline['$t' + str(i)] = 0

def rd_add(reg,var):					#only reg is added into address descr. of var and var is added into reg descr. of reg
	if var not in main.rd[reg]:
		main.ad[var].append(reg)
		main.rd[reg].append(var)


def rd_remove(reg,var):
	if reg in main.ad[var]:
		main.ad[var].remove(reg)
		main.rd[reg].remove(var)

def rd_del(var):						#register fields of a variable are cleared
	for reg in main.ad[var]:
		main.ad[var].remove(reg)
		main.rd[reg].remove(var)


def spill(reg):
	for var in main.rd[reg]:
		main.ad[var].remove(reg)
		if len(main.ad[var]) == 0 and var not in main.mem:
			print "\t" + "sw " + reg + ", " + main.memad[var]
			main.mem.append(var)
	main.rd[reg] = []

def mem_clear(var):
	if var in main.mem:
		main.mem.remove(var)

def reg_check(var,line):
	if len(main.ad[var]) == 0:
		return reg_find(line), -1
	else:
		return main.ad[var][0], 1 



def clear_ad():
	for var in main.ad:
		if var == 'return':
			continue
			
		if var not in main.mem:
			main.mem.append(var)
		main.ad[var] = []

def clear_rd():
	for reg in main.rd:
		main.rd[reg] = []

def reg_find(line):
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

def regx_get(x, y, line):

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

	return reg_find(line)

def reg_get(x,y,z,line):
	regx = regx_get(x, y, line)

	for reg in main.ad[z]:
		if main.regline[reg] != line:
			regz = reg
			main.regline[reg] = line
			return regx, regz

	regz = reg_find(line)
	return regx,regz

def update_dead(var,line):
	#print "var =" + var
	#print "line =" + str(line)
	if var != 'return' and var not in main.live[line] and (var in main.ad) and len(main.ad[var]) >0:
		if var not in main.mem:
			print "\t" + "sw " + main.ad[var][0] + ", " + main.memad[var]
			main.mem.append(var)
		for reg in main.ad[var]:
			main.rd[reg].remove(var)
			main.ad[var].remove(reg)
