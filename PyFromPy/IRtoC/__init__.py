from CTranslator import CTranslator

def generateProgram(program):
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
	translator.genStmts(function.body)
	print
	print '}'

	print
