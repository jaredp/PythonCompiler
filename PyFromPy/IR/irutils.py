from IR.ir import *
from IR.environments import *

def newrepr(ty):
	def setrepr(fn):
		ty.__repr__ = fn
		return fn
	return setrepr

@newrepr(IRIntLiteral)
@newrepr(IRFloatLiteral)
@newrepr(IRStringLiteral)
def _literalRepr(lit):
	return str(lit.value)

@newrepr(IRCode)
def _codeRepr(code):
	return code.cname

# print utils

_indentation_lvl = 0
_horizontal_rule = '-----------------'

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
	print mod.name
	print _horizontal_rule
	if mod.docstring: print 'doc:', mod.docstring
	print mod.namespace
	print 'main:', mod.initcode.cname

@pprinter(Program)
def _pprintProgram(p):
	print
	print

	for c in p.codes:
		pprint(c)

	for m in p.modules:
		pprint(m)

@pprinter(IRCode)
def _pprintIRCode(code):
	args = ['%s: %s' % a for a in zip(code.args, code.argvars)]
	print 'function %s(%s)' % (code.cname, ', '.join(args))
	print _horizontal_rule
	pprintCodeBlock(code.body)
	print
	print

@pprinter(If)
def _pprintIf(op):
	_print_indented('if %s:' % op.condition)
	_printBlockIndented(op.then)
	_print_indented('else:')
	_printBlockIndented(op.orelse)

@pprinter(Loop)
def _pprintWhile(op):
	_print_indented('loop:')
	_printBlockIndented(op.body)

@pprinter(Try)
def _pprintTry(op):
	_print_indented('try:')
	_printBlockIndented(op.body)
	if op.exception:
		_print_indented('except %s:' % op.exception)
	else:
		_print_indented('except:')
	_printBlockIndented(op.handler)

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


