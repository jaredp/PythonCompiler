from IR import *
from utils import escapeString
#from ctypes import *	-- WHY WAS THIS HERE?

class CTranslator(object):

	########################################################
	# infastructure
	########################################################

	def __init__(self, f):
		self.f = f
		self._indent = 0

	def fill(self, text = ""):
		"Indent a piece of text, according to the current indentation level"
		self.f.write('\n'+'	'*self._indent + text)

	def write(self, text):
		"Append a piece of text to the current line."
		self.f.write(text)

	def genBlock(self, block):
		self.enterBlock()
		self.genStmts(block)
		self.exitBlock()

	def enterBlock(self):
		self.write(' {')
		self._indent += 1

	def exitBlock(self):
		self._indent -= 1
		self.fill('} ')

	def genStmts(self, block):
		for stmt in block:
			if isinstance(stmt, IROperation):
				self.genOp(stmt)

			elif isinstance(stmt, IRBlockStatement):
				self.dispatch(stmt)

	def genOp(self, op):
		cppcode = self.dispatch(op)
		if isinstance(op, IRProducingOp) and op.target:
			lhs = '%s = ' % op.target
		else:
			lhs = ''
		self.fill('%s%s;' % (lhs, cppcode))


	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		meth = getattr(self, '_'+tree.__class__.__name__)
		return meth(tree)

	########################################################
	# high level generators
	########################################################

	def generateProgram(self, program):
		program.initcode.cname = 'run_main_module'

		self.writeHeader()
		for module in program.modules:
			self.declare(module.cname)
			for var in module.namespace.values():
				self.declare(var)
		self.fill()

		for function in program.codes:
			self.fill('%s;' % self.fdeclaration(function))
			self.generateFnPosCaller(function)
		self.fill()

		for function in program.codes:
			self.generateFunction(function)
		self.fill()

		'''
		TODO:
		main function that calls program.initcode,
		builds each module with P3MakeModule and P3ModuleRegisterGlobal
		'''


	def writeHeader(self):
		self.write('#include <Python.h>'); self.fill()
		self.write('#include <P3Libs.h>'); self.fill()

	def fdeclaration(self, function):
		args = ', '.join(map(self.declaration, function.argvars))
		return 'PyObject *%s(%s)' % (function.cname, args)

	def generateFnPosCaller(self, fn):
		argcount = range(len(fn.argvars))
		args = ', '.join(['PyTuple_GET_ITEM(argstuple, %s)' % i for i in argcount])
		self.fill('''
PyObject *%s_POSCALLER(PyObject *argstuple) {
	return %s(%s);
}
		''' % (fn.cname, fn.cname, args))

	def generateFunction(self, function):
		self.fill(self.fdeclaration(function))
		self.enterBlock()

		lcls = [function.namespace[lcl] for lcl in function.locals]
		for localvar in set(lcls) | function.temporaries:
			self.declare(localvar)
		self.fill()

		self.genStmts(function.body)
		self.exitBlock()

		self.fill()

	def declare(self, varname):
		self.fill('%s = NULL;' % self.declaration(varname))

	def declaration(self, varname):
		return 'PyObject *%s' % varname

	############### C Translating methods ##################
	# There should be one method per concrete grammar type #
	# Constructors should be grouped by sum type. Ideally, #
	# this would follow the order in the grammar, but	   #
	# currently doesn't.								   #
	########################################################

	def _IRIntLiteral(self, var):
		return "P3IntLiteral(%s)" % var.value

	def _IRFloatLiteral(self, var):
		return "P3FloatLiteral(%s)" % var.value

	def _IRStringLiteral(self, var):
		return 'P3StringLiteral("%s")' % escapeString(var.value)

	def _NoneLiteral(self, var):
		return 'Py_None'

	def _If(self, irexpr):
		#TODO
		self.fill('if (isTruthy(%s))' % irexpr.condition)
		self.genBlock(irexpr.then)
		if irexpr.orelse:
			self.write('else')
			self.genBlock(irexpr.orelse)

	def _Loop(self, irexpr):
		self.fill('while (1)')
		self.genBlock(irexpr.body)

	def _Return(self, irexpr):
		return "return %s" % irexpr.value

	def _Break(self, irexpr):
		return "break"

	def _Continue(self, irexpr):
		return "continue"

	def _AssignAttr(self, op):
		return (
			'P3AssignAttr(%s, "%s", %s)' % 
			(op.obj, escapeString(op.attr), op.value)
		)

	def _Attr(self, op):
		return 'P3GetAttr(%s, "%s")' % (op.obj, escapeString(op.attr))

	def _DeleteAttr(self, op):
		return 'P3DelAttr(%s, %s)' % (op.obj, obj.attr)

	def _DeleteVar(self, irexpr):
		'''
		Delete is the Python `del`, which unbinds a name.
		For now, according to the CPython C-API, the python del 
		statement translates to lowering the refcount and setting the
		variable to NULL.
		This actually raises a whole host of ugly questions about how
		to identify and handle unbound names.
		The most obvious solution is to precede all operations with a
		null-check on their operands, but this is ham-fisted as there
		are ways to show which (many) are unnecessary.
		Furthermore, the del statement is pretty rare in python code
		anyway.
		'''
		return 'Py_DECREF(%s); %s = NULL' % (irexpr.var, irexpr.var)

	def _FCall(self, fcall):
		'''
		The function calling mechanism will be among the most
		complex, and in some ways are the focus of this 
		research.  C certainly doesn't have the type of variable
		argument function calling mechanism Python does, so this
		is not a straightforward translation.
		For now, we're going to just call the _ConstCall mechanism.
		'''
		if fcall.starargs != None \
		or fcall.keystarargs != None \
		or fcall.kwargs != []: 
			raise NotImplementedError

		else:
			argcount = len(fcall.args)
			arglist = ' '.join([
				'PyTuple_SET_ITEM(args, %s, %s);' % a
				for a in zip(range(argcount), fcall.args)
			])
			return (
				'P3Call(%s, ({PyObject *args = PyTuple_New(%s);%s args;}))'
				% (fcall.fn, argcount, arglist)
			)

	def _MethodCall(self, irexpr):
		'''
		This is the _FCall mechanism, with all the added fun of
		class attribute lookup.  It's entirely possible we wont
		get to classes, and not get to this.
		'''
		raise NotImplementedError

	def _ConstCall(self, irexpr):
		args = ', '.join(map(repr, irexpr.args))
		return '%s(%s)' % (irexpr.fn, args)
	
	def _Assign(self, irexpr):
		return repr(irexpr.rhs)

	#Take IRClass/IRFunction/IRModule and turn them into py objects:
	def _MakeFunction(self, op):
		return (
			'P3MakeFunction((fptr)%s_POSCALLER, "%s")'
			% (op.code.cname, op.code.pyname)
		)

	def _MakeClass(self, op):
		'''
		These properly should be structs defined at top-level
		Same for modules.
		This should just get them.
		For now, we're actually going to make them with the
		fallback usually reserved for type(,,)
		'''
		return 'P3MakeClass(%s)' % op.klass.name

	def _GetModule(self, op):
		return op.module.cname

	# exception handling
	def _Try(self, irexpr):
		raise NotImplementedError

	def _Raise(self, irexpr):
		raise NotImplementedError
	
	def _GetException(self, irexpr):
		raise 'P3GetException()'

	# generator handling
	def _Yield(self, irexpr):
		'''
		Generators are considerably complicated,
		and require tricky C generation support.
		Yield is not a keyword in C/C++
		'''
		raise NotImplementedError
	
	def _GetGeneratorSentIn(self, irexpr):
		raise NotImplementedError




