
import ast
from _ast import *
from utils import *
from astutils import *

class TempVar(AST):
	nextnum = 0
	def __init__(self, nameSuggestion=''):
		self.num = TempVar.nextnum
		TempVar.nextnum += 1
		self.name = nameSuggestion+'$'+str(self.num)
		
	def __repr__(self):
		return self.name


def checkNoExecs(m):
	pass

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

@perStatement
def removeNoneStmts(stmt):
	if stmt != None:
		yield stmt

@perStatement
def makePrintAFunction(stmt):
	if isinstance(stmt, Print):
		for val in stmt.values:
			yield Expr(mkVanillaCall("print", [stmt.dest, val]))
		if stmt.nl:
			yield Expr(mkVanillaCall("printnl", []))
	else:
		yield stmt

@perFunction
def setFnDocstrings(fn):
	if len(fn.body) > 0 and matches(fn.body[0], Expr(Str)):
		fn.docstring = fn.body[0].value.s
		fn.body = fn.body[1:]
	else:
		fn.docstring = None


@perFunction
def setLocals(fn):
	fn.locals = {lcl: TempVar(lcl) for lcl in getLocals(fn.body)}
	fn.temps = fn.locals.values()

#similar analysis needs to be done for closures, globals
#closure handling is *difficult*

@perExprInFunc
def extractSubexprs(e, block, fn):
	if isinstance(e, Name):
		#lookup routine: locals, captures, globals, I think
		if e.id in fn.locals:
			return fn.locals[e.id]
		else:
			return e

	else:
		return e

def transformModule(m):
	removeLineNos(m)
		
	checkNoExecs(m)

	extractLoadFunction(m)
	#somewhere around here, extract nested functions
	#I believe this should include methods in some form
	
	removeNoneStmts(m)
	setFnDocstrings(m)
	makePrintAFunction(m)
	#makeReprAFunction(m)
	#makeAssertAFunction(m)
	
	setLocals(m)
	extractSubexprs(m)


#makes certain debugging easier
def removeLineNos(m):
	for n in allchildren(m):
		if hasattr(n, 'lineno'):
			del n.lineno
		if hasattr(n, 'col_offset'):
			del n.col_offset


def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

