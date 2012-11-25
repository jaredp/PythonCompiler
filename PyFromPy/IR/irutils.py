from IR.ir import *
from IR.environments import *

IRIntLiteral.__repr__ = IRFloatLiteral.__repr__ = IRStringLiteral.__repr__ = \
	lambda l: str(l.value)

# print utils

_indentation_lvl = 0

def _indent():
	global _indentation_lvl
	_indentation_lvl += 1
	
def _dedent():
	global _indentation_lvl
	_indentation_lvl -= 1

def _print_indented(s):
	print '   '*_indentation_lvl + s

# printers

def pprint(obj):
	if hasattr(obj, 'pprint'):
		obj.pprint()
	else:
		_print_indented(repr(obj))

def pprintCodeBlock(codeblock):
	for op in codeblock:
		pprint(op)

def _printBlockIndented(block):
	_indent()
	pprintCodeBlock(block)
	_dedent()

def pprinter(t):
	def setpprint(newppfn):
		t.pprint = newppfn
		return newppfn	#so we can chain them
	return setpprint

@pprinter(IRModule)
def _pprintMod(mod):
	print mod.namespace
	print 'main:'
	pprintCodeBlock(mod.initcode.body)

@pprinter(If)
def _pprintIf(op):
	_print_indented('if %s:' % op.condition)
	_printBlockIndented(op.then)
	_print_indented('else:')
	_printBlockIndented(op.orelse)

@pprinter(FCall)
@pprinter(ConstCall)
def _pprintCall(call):
	if call.target:
		asn = repr(call.target) + ' = '
	else:
		asn = ''
	args = ', '.join([repr(a) for a in call.args])
	_print_indented('%s%s(%s)' % (asn, call.fn, args))


@pprinter(Assign)
def _pprintAssign(asn):
	_print_indented('%s = %s' % (asn.target, asn.rhs))


