from CTranslator import CTranslator

def generateProgram(program):
	for function in program.codes:
		generateFunction(function)

def generateFunction(function):
	translator = CTranslator()

	args = ', '.join(map(repr, function.argvars))
	print 'PyObject *%s(%s) {' % (function.cname, args),
	#FIXME: somewhere here, put the args
	translator.genStmts(function.body)
	print
	print '}'

	print
