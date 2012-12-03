from CTranslator import CTranslator

def generateProgram(program):
	for function in program.codes:
		generateFunction(function)

def generateFunction(function):
	
	#define locals and globals

	translator = CTranslator()

	args = ', '.join(map(repr, function.argvars))
	print 'PyObject *%s(%s) {' % (function.cname, args),
	#FIXME: somewhere here, put the locals
	translator.genStmts(function.body)
	print
	print '}'

	print
