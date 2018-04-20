class SymTable(object):

	id = 1
	def __init__(self, name="main", parent=None):

		self.id = SymTable.id

		SymTable.id+=1
		self.nested_scopes=[]   #List of all symbol tables whose scope are within this symbol table
		self.symbols = {}	   #Dictionary to hold the attributes and names of all symbols
		self.functions = {}		#Dictionary to hold functions name and attributes
		self.offset = 0			# Byte Storage offset for this scope

		self.parent = parent
		
		if self.parent != None:
			self.parent.nested_scopes.append(self)


	def add_function(self, function_name, function_attr):

		self.functions[function_name] = function_attr

	def add_symbol(self, sym_name, sym_attr):

		self.symbols[sym_name] = sym_attr

	def find_var_decl(self, var):
		temp = self
		flag = 0
		
		while(temp is not None):
			if var in temp.symbols:
				flag = 1
				break
			temp = temp.parent

		return (flag,temp)

	def find_func_decl(self, function):
		temp = self
		flag = 0
		
		while(temp is not None):
			if function in temp.function:
				flag = 1
				break
			temp = temp.parent

		return (flag,temp)