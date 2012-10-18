
from _ast import *


def compose(f):
	def inner(g):
		def wrapper(*args, **kwargs):
			return f(g(*args, **kwargs))
		return wrapper
	return inner

def flattenList(l):
	for i in l:
		for j in i:
			yield j

#############################################################
# AST constructors
#############################################################

def mkVanillaFunction(fname, argnames, body):
	args = arguments([Name(arg, Param()) for arg in argnames], None, None, [])
	return FunctionDef(fname, args, body, [])

def mkVanillaCall(fname, args):
	return Call(Name(fname, Load), args, [], None, None)


#############################################################
# AST traversal
#############################################################

def transformBlocks(node, transform):
	# this should really walk the tree explicitly...
	children = node.__dict__
	for attr in children:
		child = children[attr]
		if child == []:	
			continue #no transform([])
		elif type(child) == list:
			for e in child: transformBlocks(e, transform)
			if isinstance(child[0], stmt):
				children[attr] = list(transform(child))
		elif hasattr(child, '__dict__'):
			transformBlocks(child, transform)

def forEachBlock(fn):
	def wrapper(node):
		transformBlocks(node, fn)
	return wrapper

def forEachStatement(fn):
	@forEachBlock
	def wrapper(stmts):
		for stmt in stmts:
			for newstmt in fn(stmt):
				yield newstmt
	return wrapper

def allchildren(node):
	if isinstance(node, AST): children = node.__dict__.values()
	elif type(node) == list:  children = node
	else: return
		
	for child in children:
		for grandchild in allchildren(child):
			yield grandchild
		if isinstance(child, AST):
			yield child


def getAllOf(subnodetype, node):
	for subexpr in allchildren(node):
		if isinstance(subexpr, subnodetype):
			yield subexpr

