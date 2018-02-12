#!/usr/bin/python



'''
Class Quadruple contains 3AC in list of list data structure
self.data[lineNo][0] contains block number
self.data[lineNo][1] contains line number

Methods for - Liveness information, Basic Block Information, Next Use information

'''

class IR_Data(object):

    def __init__(self):
        self.Data = []
        self.NumBlocks = 0
        self.Identifiers = {}          #List of all the identifiers(Only integers or functions for our purpose) in the IR CODE,

        self._Assignment = ['=']        
        self._Operators = ["+" , "-" , "*" , "/"]
        self._Rel_Ops = [ '&' , '|' , '^', '<=' , '>=' , '<' , '>' , '==', '!=']
        self._Functions = [ 'call' , 'ret' ]        
        self._Branches = ['goto' ,  'ifgoto']
        self._Library_Functions = ['scan' , 'print']
        self._Array_Declarations = ['Array']

    '''
    load3AC - 3AC is loaded into Quadruple object
    Args:
        filename - file where the 3AC is stored
    
    Returns/Modifies:
        self.data - this is where the 3AC is stored
    '''

    def load3AC(self, filename):
        f = open(filename, 'r')
        i = 1
        self.Data.append([])       # empty list added at the beginning to keep list index and line numbers consistent

        for line in f:
            self.Data.append([0])          #0 is placeholder for block number, which will be assigned by assignBlocks method
            currLine = line.split()
            self.Data[i] = self.Data[i] + currLine
            VarList,TypeList = self.extIds(currLine)

            temp = 0
            i+=1

            for v in VarList:
                self.Identifier[v] = TypeList[temp]
                temp += 1


    '''
    extIds:   extracts identifiers from a given line
    
    Args:
        line - Input string, sent as list
    
    Returns/Modifies:
        VarList : List of variables present in the line
        TypeList    : List of types of the corresponding variables
    '''
    def extIds(self,line):
        self.VarList_Operands = []
        self.VarList_Destination = []
        #TypeList = []               Since all variables have type integer for our purpose No Consideration to be done here
        #return VarName, Type
        
        pass


    '''
    assignBlocks - Assigns Block Numbers to every 3AC line

    Args:
        none

    Returns/Modifies:
        self.data[lineNo][0] - this is where block number is assigned

    '''
    def assignBlocks(self):
        size = len(self.Data)
        block = []   # temporary list to store information about leaders in 3AC
        for i in range(0,size):
            block.append(0)       
        
        #Assign 1 to all leaders in 3AC    
        for i in range(1,size):
            if(self.Data[i][2] == 'label'):
                block[i] = 1
            else:
                if (self.Data[i][2] == 'call' or self.Data[i][2] == 'ret'):
                    if(i+1 <= size-1):
                        block[i+1] = 1
                else:
                    if (self.Data[i][2] == 'goto' or self.Data[i][2] == 'ifgoto'):
                        if(i+1 <= size-1):
                            block[i+1] = 1
                            block[int(self.Data[i][3])] = 1
        
        block[1] = 1  # First instruction is a leader

        for i in range(1,size):
            if (block[i] == 1):
                self.NumBlocks += 1

            self.data[i][0] = self.NumBlocks

        self.Num_Lines = len(self.Data) -1

        #Get Line wise 
        Blocks = [ t[0] for t in self.Data[1:] ]  #Line wise block numbers

        self.Block_Start = [-1]          # -1 is inserted so that 0 indexing is tackled and we are able to index using line numbers
        self.Block_End = [-1]           # -1 is inserted so that 0 indexing is tackled and we are able to index using line numbers

        temp = 1
        flag = 0


        for index in range(len(Blocks)):

            if( index == len(Blocks) ):
                self.Block_End.append(temp)
                del temp
                del flag
                break

            if( Blocks[index] == temp and flag == 0):
                self.Blocks_Start.append(index)
                flag = 1
                continue


            if( index + 1 == len(Blocks) and Blocks[index+1] != temp and flag == 1):
                self.Blocks_End.append(index)
                flag = 0
                temp +=1

    '''
        I_type determines the type of instruction

        self._Operators = ["+" , "-" , "*" , "/"]
        self._Rel_Ops = [ '&' , '|' , '^', '<=' , '>=' , '<' , '>' , '==', '!=']
        self._Functions = [ 'call' , 'ret' ]        
        self._Branches = ['goto' ,  'ifgoto']
        self._Library_Functions = ['scan' , 'print']
        self._Array_Declarations = ['Array']
    '''
    def I_Type(Instruction):
        temp = Instruction[0]

        if temp in self._Functions:
            return 'F'  #Function

        if temp in self._Branches:
            return 'B'  #Branching
        
        if temp in self._Assignment and len(Instruction) == 3:
            return 'A'  #Assignment

        if temp in self._Operators:
            return 'O'
        

    '''
    Liveness - Generates Liveness information of variables
    '''    
    def Liveness(self):
        self.Live = []       # List of list containing variables live at a line i
        
        #Populating the list with empty lists
        for t in range( len(self.Data) ):
            self.Live.append([])

        for index in range(self.NumBlocks, 0, -1):

            L_Start = self.Blocks_Start[index]
            L_End = self.Blocks_End[index]

            for lno in range(L_End, L_Start-1,-1):
                line = self.Data[lno]
                instruction = line[2:]   # Actual Instruction

            

