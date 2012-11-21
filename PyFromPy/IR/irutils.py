from IR.ir import *


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

def pprintCodeBlock(codeblock):
	for op in codeblock:
		op.pprint()

def _printBlockIndented(block):
	_indent()
	pprintCodeBlock(block)
	_dedent()

def _pprintOp(op):
	_print_indented(repr(op))
IROperation.pprint = _pprintOp

def _pprintMod(mod):
	print mod.namespace
	print 'functions:', mod.functions
	print 'main:'
	pprintCodeBlock(mod.toplevel)
IRModule.pprint = _pprintMod

def _pprintIf(op):
	_print_indented('if %s:' % op.condition)
	_printBlockIndented(op.then)
	_print_indented('else:')
	_printBlockIndented(op.orelse)
If.pprint = _pprintIf
