from IR import *
from base import *

def generateProgram(program):
	program.initcode.cname = 'run_main_module'

	write('#include <P3Libs.h>')
	fill()

	for module in program.modules:
		fill('DECLARE_MODULE(%s, "%s");' % (module.cname, module.name))
		for var in module.namespace.values():
			fill('DECLARE_GLOBAL(%s);' % var)
	fill()

	fill('void register_globals()')
	enterBlock()
	for module in program.modules:
		fill('P3InitModule((P3Module *)%s);' % module.cname)
		for gbl_id, var in module.namespace.items():
			# the gbl##_Cell is to match DECLARE_GLOBAL in pylib/modules.h
			fill('P3ModuleRegisterGlobal(%s, "%s", &%s_Cell);' % (
				module.cname, gbl_id, var
			))
		fill()
	exitBlock()
	fill()


	for function in program.codes:
		fill('%s;' % fdeclaration(function))
		generateFnPosCaller(function)
	fill()

	for function in program.codes:
		generateFunction(function)
	fill()


def fdeclaration(function):
	return 'PyObject *%s(%s)' % (
		function.cname,
		', '.join(['PyObject *%s' % v for v in function.argvars])
	 )

def generateFnPosCaller(fn):
	argcount = range(len(fn.argvars))
	fill('PyObject *%s_POSCALLER(PyObject *argstuple) {' % fn.cname)
	fill('	return %s(%s);' % (
		fn.cname,
		', '.join(['PyTuple_GET_ITEM(argstuple, %s)' % i for i in argcount])
	))
	fill('}')

def generateFunction(function):
	fill(fdeclaration(function))
	enterBlock()

	lcls = [function.namespace[lcl] for lcl in function.locals]
	for localvar in set(lcls) | function.temporaries:
		fill('PyObject *%s = NULL;' % localvar)
	fill()

	genStmts(function.body)
	exitBlock()

	fill()
