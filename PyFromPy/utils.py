
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


#############################################################
# Pattern matching
#############################################################

ig, igs  = object(), object()
class inverse:
	def __init__(self, pattern):
		self.pattern = pattern
'''
ig				matches anything
igs				is ment to match 0+ things 
[igs]			matches any list
[n, igs]		matches a list that starts with n
[igs, n]		matches a list that ends in n
[igs, n, igs]	matches a list that contains n
inverse(n)		matches iff it's not n
'''

def matches(node, pattern):
	if pattern == ig:				return True
	if type(pattern) == inverse:	return not matches(node, pattern.pattern)
	if type(node) != type(pattern): return False
	
	if type(node) in [list, tuple]:
		if pattern == []:
			return node == []
		elif pattern[0] == igs and pattern[-1] == igs:
			return all(
				any(matches(e, p) for e in node)
				for p in pattern[1:-1]
			)
		elif pattern[-1] == igs:
			pattern = pattern[:-1]
			if len(pattern) > len(node): return False
			node = node[:len(pattern)]
			
		elif pattern[0] == igs:
			pattern = pattern[1:]
			if len(pattern) > len(node): return False
			node = node[-len(pattern):]
			
		return len(node) == len(pattern) and all(
			matches(n, p) for (n, p) in
			zip(node, pattern)
		)
	
	elif hasattr(node, '__dict__'):
			for k, v in pattern.__dict__.items():
				if not matches(node.__dict__[k], v):
					return False
			return True
	
	else:
		return node == pattern
			
			
			