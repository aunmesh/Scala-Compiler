import LEXER
import sys
import os
import re
import ply.yacc as yacc
from GRAMMAR3 import *




tokens = LEXER.tokens




parser = yacc.yacc()

fname = sys.argv[1]

prog = fopen(fname, "r").read()
f.close()
root = parser.parse(prog)


Current_Derivation = ['compilationUnit']

def printTree(node, file):
	global Current_Derivation

	if(len(node.children) == 0 ):
		return 

	L = list(reversed(Current_Derivation))
	index_node = L.index(str(node.name))

	Children = []
	for n in node.children:
		Children.append(str(n.name))

	# Modifying the Current_Derivation variable to include the children of node and removing node
	Current_Derivation = Current_Derivation[:index_node] + Children + Current_Derivation[index_node+1:]


	if node.name not in LEAF_NODES:  #Node is not a leaf node
		L = list(reversed(Current_Derivation))
		index_rightchild = L.index(str(Children[-1].name)) 
		Part1 = " ".join(Current_Derivation[:index_node])   #Yet to be derived
		Part2 = " ".join(Current_Derivation[index_node:index_rightchild])	   #Just derived
		Part3 = Current_Derivation[index_rightchild]  # Will be derived next
		Part4 = " ".join(Current_Derivation[index_rightchild+1:]) #Already derived
		print >>> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font>"

		for n in list(reversed(Children)):
			printTree(n, file)

	else:  #Node is a leaf node
		if(index_node != 0):
			Part1 = " ".join(Current_Derivation[:index_node-1]) #Yet to be derived
			Part2 = Current_Derivation[index_node-1]  #Will be derived next
			Part3 = Children[-1]      #Just derived
			Part4 = " ".join(Current_Derivation[index_rightchild+1:]) #Already derived

			print >>> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font>"
		else:
			Part1 = "" #Yet to be derived
			Part2 = "" #Will be derived next
			Part3 = Children[-1] #Just derived
			Part4 = " ".join(Current_Derivation[index_rightchild+1:]) #Already derived
			print >>> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font>"


file = open(sys.argv[1][5:-6] + ".html","w+")
if node:
	print >> file,'''<!DOCTYPE html>
<html>
<body>'''
	print >>file,"<b>" , Current_Derivation[0],"</b> <br><br>"
	printTree(root,file)
	print >> file, '''</body>
</html>'''

file.close()

