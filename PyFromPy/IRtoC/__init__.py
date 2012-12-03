from CTranslator import CTranslator

def generateProgram(program):
	#TOFIX: namespace is an IRVAR with a single value, or is value a collection of different values??
	for module in program.modules:
		for val in module.namespace.value:

	for function in program.codes:
		generateFunction(function)

	#define locals and globals
	#PyObject *a$0;
	#locals: IRCode.temporaries
	#globals: IRModule.namespace.values()

def generateFunction(function):
	
	translator = CTranslator()

	args = ', '.join(map(repr, function.argvars))
	print 'PyObject *%s(%s) {' % (function.cname, args),
	#FIXME: somewhere here, put the args
	for localvar in function.temporaries:
		print 'PyObject *%s = NULL;' % (localvar.name),

	translator.genStmts(function.body)
	print
	print '}'

	print
