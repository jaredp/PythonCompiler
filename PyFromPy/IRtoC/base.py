from IR import *

def setup(out):
	global f
	global _indent
	
	f = out
	_indent = 0


def fill(text = ""):
	"Indent a piece of text, according to the current indentation level"
	f.write('\n'+'	'*_indent + text)

def write(text):
	"Append a piece of text to the current line."
	f.write(text)

def genBlock(block):
	enterBlock()
	genStmts(block)
	exitBlock()

def enterBlock():
	global _indent
	write(' {')
	_indent += 1

def exitBlock():
	global _indent
	_indent -= 1
	fill('} ')

def genStmts(block):
	for stmt in block:
		if isinstance(stmt, IROperation):
			genOp(stmt)

		elif isinstance(stmt, IRBlockStatement):
			dispatch(stmt)

def genOp(op):
	cppcode = dispatch(op)
	if isinstance(op, IRProducingOp) and op.target:
		lhs = '%s = ' % op.target
	else:
		lhs = ''
	fill('%s%s;' % (lhs, cppcode))


import instr_translations
dispatch_table = instr_translations.__dict__

def dispatch(tree):
	return dispatch_table['_'+tree.__class__.__name__](tree)
