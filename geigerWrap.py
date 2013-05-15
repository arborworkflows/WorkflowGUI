# GeigerWrapper module 

# This module wraps calls to Geiger so that a python program can make calls to Geiger for 
# an embedded R instance to process phylogenetic trees.  
# 

import rpy2.robjects as robjects

# initialize a global variable to store trees
gw_trees = []
gw_numTrees = 0

def gw_InitGeiger():
	robjects.r("library('geiger')")
	r = robjects.r

def gw_ShutdownGeiger():
	print("placeholder for R / Geiger shutdown")
	
def gw_readNewickTree(filename):	
	# for now lets just read a tree so the R interpreter has something defined in it
	newtree = robjects.r('read.tree(filename) -> myTree')
	return newtree
	

	
	