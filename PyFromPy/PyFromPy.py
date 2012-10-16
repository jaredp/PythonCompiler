
import ast
from _ast import *
from unparse import Unparser
from gencpp import CppGenerator

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

def mkVanillaFunction(fname, argnames, body):
	args = arguments([Name(arg, Param()) for arg in argnames], None, None, [])
	return FunctionDef(fname, args, body, [])

def mkVanillaCall(fname, args):
	return Call(Name(fname, Load), args, [], None, None)

def extractLoadFunction(mod):
	imports, fns, classes, init = [], [], [], []
	for stmt in mod.body:
		if isinstance(stmt, Import) or isinstance(stmt, ImportFrom):
			imports.append(stmt)
		elif isinstance(stmt, FunctionDef):
			fns.append(stmt)
		elif isinstance(stmt, ClassDef):
			classes.append(stmt)
		elif isinstance(stmt, Return):
			raise 'syntax error: return outside a function'
		else:
			init.append(stmt)
	
	loadfn = mkVanillaFunction('load', [], init)
	fns.append(loadfn)
	
	mod.body = imports + classes + fns

def transformBlocks(node, transform):
	# this should really walk the tree explicitly...
	children = node.__dict__
	for attr in children:
		child = children[attr]
		if type(child) == list:
			if len(child) == 0:	continue	#no transform([])
			if isinstance(child[0], stmt):
				children[attr] = list(transform(child))
			else:
				for e in child:
					transformBlocks(e, transform)
		else:
			if hasattr(child, '__dict__'):
				transformBlocks(child, transform)
			else:
				print child

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

@forEachStatement
def removeNoneStmts(stmts):
	if stmt != None:
		yield stmt

@forEachStatement
def makePrintAFunction(stmt):
	if isinstance(stmt, Print):
		for val in stmt.values:
			yield mkVanillaCall("print", [stmt.dest, val])
		if stmt.nl:
			yield mkVanillaCall("printnl", [])
	else:
		yield stmt

class TempVar(AST):
	nextnum = 0
	def __init__(self):
		self.num = TempVar.nextnum
		TempVar.nextnum += 1

from gencpp import CppGenerator

tfile = '/Users/Jared/Dropbox/Development/PythonCompiler/fib.py'
if __name__ == '__main__':
	mod = parseFile(tfile)
	
	extractLoadFunction(mod)
	removeNoneStmts(mod)
	makePrintAFunction(mod)
	
	CppGenerator(mod)
	
	print
	print
