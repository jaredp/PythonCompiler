
import ast
from _ast import *
from unparse import Unparser
from gencpp import CppGenerator
from utils import *

class TempVar(AST):
	nextnum = 0
	def __init__(self):
		self.num = TempVar.nextnum
		TempVar.nextnum += 1

class ExprSeq(expr):
	def __init__(self, stmts, expr):
		self.stmts = stmts
		self.expr = expr

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

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

def getLocals(fnbody):
	stores = [name.id for name
			  in getAllOf(Name, fnbody) 
			  if type(name.ctx) in [Store, AugStore]]
	gbls = flattenList(gdecl.names for gdecl in getAllOf(Global, fnbody))
	return list(set(stores) - set(gbls))

@forEachStatement
def removeNoneStmts(stmt):
	if stmt != None:
		yield stmt

@forEachStatement
def makePrintAFunction(stmt):
	if isinstance(stmt, Print):
		for val in stmt.values:
			yield Expr(mkVanillaCall("print", [stmt.dest, val]))
		if stmt.nl:
			yield Expr(mkVanillaCall("printnl", []))
	else:
		yield stmt


tfile = '../examples/fib.py'
def main():
	m = parseFile(tfile)
	
	extractLoadFunction(m)
	removeNoneStmts(m)
	makePrintAFunction(m)
	
	for fn in getAllOf(FunctionDef, m):
		fn.locals = getLocals(fn.body)
	
	CppGenerator(m)
	
	print
	print


if __name__ == '__main__':
	from debug import print_exc_plus
	try:
		main()
	except:
		print_exc_plus()
