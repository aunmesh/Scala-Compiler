#!/usr/bin/python
import lexer as LEXER
import sys
import os
import re
import ply.yacc as yacc
from Grammar4 import *

tokens = LEXER.tokens


#ERROR
def p_error(p):
  
	flag=-1;

	print("Syntax error at '%s'" % p.value)
	print('\t Error: {}'.format(p))



parser = yacc.yacc()

fname = sys.argv[1]

f = open(fname, "r")

prog = f.read()

f.close()

root = parser.parse(prog)

Current_Derivation = ['compilationUnit']


def printTree(node, file):
	global Current_Derivation

	if(len(node.children) == 0 ):
		return

	Prev_Derivation = Current_Derivation
	L = list(reversed(Current_Derivation))
	
	index_node = L.index(str(node.name))
	index_node = len(Current_Derivation) - index_node -1

	Children = []
	for n in node.children:	
		Children.append(str(n.name))

	# Modifying the Current_Derivation variable to include the children of node and removing node
	Current_Derivation = Current_Derivation[:index_node] + Children + Current_Derivation[index_node+1:]
	#print "OLD Derivation " +  str(Current_Derivation)

	if node.name not in LEAF_NODES:  #Node is not a leaf node
		L = list(reversed(Current_Derivation))
		index_rightchild = L.index(str(node.children[-1].name))
		index_rightchild = len(Current_Derivation) - index_rightchild - 1
		Part1 = " ".join(Current_Derivation[:index_node])   #Yet to be derived
		Part2 = " ".join(Current_Derivation[index_node:index_rightchild])	   #Just derived
		Part3 = Current_Derivation[index_rightchild]  # Will be derived next
		Part4 = " ".join(Current_Derivation[index_rightchild+1:]) #Already derived
		print >> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font> <br> <br>"

		for n in list(reversed(node.children)):
			printTree(n, file)

	else:  #Node is a leaf node
		if(index_node != 0):
			Part1 = " ".join(Current_Derivation[:index_node-1]) #Yet to be derived
			Part2 = Current_Derivation[index_node-1]  #Will be derived next
			Part3 = Children[-1]      #Just derived
			Part4 = " ".join(Prev_Derivation[index_node+1:]) #Already derived

			print >> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font> <br> <br>"
		else:
			Part1 = "" #Yet to be derived
			Part2 = "" #Will be derived next
			Part3 = Children[-1] #Just derived
			Part4 = " ".join(Prev_Derivation[index_node+1:]) #Already derived
			print >> file, str(Part1) + "<font color=\"blue\"> " + str(Part2) + "<b>" + str(Part3) + "</font> </b>" + "<font color=\"red\"> " + str(Part4)+ "</font> <br> <br>"


	return


file = open(sys.argv[1][5:-6] + ".html","w+")
if root:
	print >> file,'''<!DOCTYPE html>
<html>
<body>'''
	print >>file,"<b>" , Current_Derivation[0],"</b> <br><br>"
	printTree(root,file)
	print >> file, '''</body>
</html>'''

file.close()

