from IR import *
from base import *

def generateProgram(program):
	program.initcode.cname = 'run_main_module'

	write('#include <P3Libs.h>'); fill()

	for module in program.modules:
		declare(module.cname)
		for var in module.namespace.values():
			declare(var)
	fill()

	for function in program.codes:
		fill('%s;' % fdeclaration(function))
		generateFnPosCaller(function)
	fill()

	for function in program.codes:
		generateFunction(function)
	fill()


def fdeclaration(function):
	args = ', '.join(map(declaration, function.argvars))
	return 'PyObject *%s(%s)' % (function.cname, args)

def generateFnPosCaller(fn):
	argcount = range(len(fn.argvars))
	args = ', '.join(['PyTuple_GET_ITEM(argstuple, %s)' % i for i in argcount])
	fill('''
PyObject *%s_POSCALLER(PyObject *argstuple) {
return %s(%s);
}
	''' % (fn.cname, fn.cname, args))

def generateFunction(function):
	fill(fdeclaration(function))
	enterBlock()

	lcls = [function.namespace[lcl] for lcl in function.locals]
	for localvar in set(lcls) | function.temporaries:
		declare(localvar)
	fill()

	genStmts(function.body)
	exitBlock()

	fill()

def declare(varname):
	fill('%s = NULL;' % declaration(varname))

def declaration(varname):
	return 'PyObject *%s' % varname

