from _ast import *
from utils import *

#############################################################
# AST traversal
#############################################################

stmtComponents = {
	FunctionDef: ['name', 'args', 'body', 'decorator_list'],
	ClassDef: ['name', 'bases', 'body', 'decorator_list'],
	Return: ['value'],
	
	Delete: ['targets'],
	Assign: ['targets', 'value'],
	AugAssign: ['target', 'op', 'value'],
	
	Print: ['dest', 'values', 'nl'],
	
	For: ['target', 'iter', 'body', 'orelse'],
	While: ['test', 'body', 'orelse'],
	If: ['test', 'body', 'orelse'],
	With: ['context_expr', 'optional_vars', 'body'],
	
	Raise: ['type', 'inst', 'tback'],
	TryExcept: ['body', 'handlers', 'orelse'],
	TryFinally: ['body', 'finalbody'],
	Assert: ['test', 'msg'],
	
	Import: ['names'],
	ImportFrom: ['module', 'names', 'level'],
	
	Global: ['names'],
	Expr: ['value'],
	Pass: [], Break: [], Continue: []
}

exprComponents = {
	BoolOp: ['op', 'values'],
	BinOp: ['left', 'op', 'right'],
	UnaryOp: ['op', 'operand'],
	Lambda: ['args', 'body'],
	IfExp: ['test', 'body', 'orelse'],
	Dict: ['keys', 'values'],
	Set: ['elts'],
	ListComp: ['elt', 'generators'],
	SetComp: ['elt', 'generators'],
	DictComp: ['key', 'value', 'generators'],
	GeneratorExp: ['elt', 'generators'],
	Yield: ['value'],
	Compare: ['left', 'ops', 'comparators'],
	Call: ['func', 'args', 'keywords'],
	Repr: ['value'],
	Num: ['n'],
	Str: ['s'],
	Attribute: ['value', 'attr', 'ctx'],
	Subscript: ['value', 'slice', 'ctx'],
	Name: ['id', 'ctx'],
	List: ['elts', 'ctx'],
	Tuple: ['elts', 'ctx'],
}
	
#	expr_context = Load | Store | Del | AugLoad | AugStore | Param
	
#	slice = Ellipsis | Slice(expr? lower, expr? upper, expr? step)
#		  | ExtSlice(slice* dims)
#		  | Index(expr value)
	
#	boolop = And | Or
	
#	operator = Add | Sub | Mult | Div | Mod | Pow | LShift
#	| RShift | BitOr | BitXor | BitAnd | FloorDiv
	
#	unaryop = Invert | Not | UAdd | USub
	
#	cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
	
#	comprehension = (expr target, expr iter, expr* ifs)
	
#	excepthandler = ExceptHandler(expr? type, expr? name, stmt* body)
#	attributes (int lineno, int col_offset)
	
#	arguments = (expr* args, identifier? vararg,
#	identifier? kwarg, expr* defaults)
	
#	keyword = (identifier arg, expr value)
	
#	alias = (identifier name, identifier? asname)


#############################################################
# AST constructors
#############################################################

def mkVanillaFunction(fname, argnames, body):
	args = arguments([Name(arg, Param()) for arg in argnames], None, None, [])
	return FunctionDef(fname, args, body, [])

def mkVanillaCall(fname, args):
	return Call(Name(fname, Load), args, [], None, None)

#############################################################
# AST walkers
#############################################################

def transformBlocks(node, transform, *args, **kwargs):
	# this should really walk the tree explicitly...
	if not hasattr(node, '__dict__'):
		return
	
	children = node.__dict__
	for attr in children:
		child = children[attr]
		if child == []:	
			continue #no transform([])
		elif type(child) == list:
			for e in child: transformBlocks(e, transform, *args, **kwargs)
			if isinstance(child[0], stmt):
				children[attr] = list(transform(child, *args, **kwargs))
		elif hasattr(child, '__dict__'):
			transformBlocks(child, transform, *args, **kwargs)

def perBlock(fn):
	def wrapper(node):
		transformBlocks(node, fn)
	return wrapper

def perStatement(fn):
	@perBlock
	def wrapper(stmts):
		for stmt in stmts:
			for newstmt in fn(stmt):
				yield newstmt
	return wrapper

def perFunction(fn):
	def wrapper(m):
		for decl in m.body:
			if isinstance(decl, FunctionDef):
				fn(decl)
	return wrapper

#should only be used in perExpr
def perSubexpr(fn, e, block, *args, **kwargs):
	if type(e) == list:
		return [
				perSubexpr(fn, subexpr, block, *args, **kwargs)
				for subexpr in e
				]
	
	if isinstance(e, expr):
		subexprs = e.__dict__
		for attr in subexprs:
			subexprs[attr] = perSubexpr(fn, subexprs[attr], block, *args, **kwargs)
	
	e = fn(e, block, *args, **kwargs)
	return e

def perExpr(fn, *args, **kwargs):
	@perBlock
	def wrapper(stmts):
		newstmts = []
		for s in stmts:
			children = s.__dict__
			for attr in children:
				child = children[attr]
				if isinstance(child, expr):
					children[attr] = perSubexpr(fn, child, newstmts, *args, **kwargs)
				if isinstance(child, list):
					children[attr] = [
									  perSubexpr(fn, e, newstmts, *args, **kwargs)
									  for e in child
									  ]
			newstmts.append(s)
		return newstmts
	return wrapper

def perExprInFunc(transform):
	@perFunction
	def wrapper(fn):
		return perExpr(transform, fn)(fn)
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
