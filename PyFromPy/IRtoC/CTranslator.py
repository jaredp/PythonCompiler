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
		if isinstance(op, IRProducingOp) and op.target:
			self.fill('%s = ' % op.target)
		else:
			self.fill()

		self.dispatch(op)
		self.write(';')


	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		meth = getattr(self, '_'+tree.__class__.__name__)
		return meth(tree)

	def translateExpr(s, irexpr):
		meth = getattr(s, '_'+irexpr.__class__.__name__)
		return meth(irexpr)

	########################################################
	# high level generators
	########################################################

	def generateProgram(self, program):
		program.initcode.cname = 'run_main_module'

		self.writeHeader()
		for module in program.modules:
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
		self.write("P3IntLiteral(%s)" % var.value)

	def _IRFloatLiteral(self, var):
		self.write("P3FloatLiteral(%s)" % var.value)

	def _IRStringLiteral(self, var):
		self.write('P3StringLiteral("%s")' % escapeString(var.value))

	def _NoneLiteral(self, var):
		self.write('Py_None')

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

	def _Try(self, irexpr):
		#TODO
		#TOFIX: What's our strategy for exception handling?
		pass

	def _Return(self, irexpr):
		self.write("return %s" % irexpr.value)

	def _Yield(self, irexpr):
		'''
		Generators are considerably complicated,
		and require tricky C generation support.
		Yield is not a keyword in C/C++
		'''
		raise NotImplementedError

	def _Raise(self, irexpr):
		self.fill('raise ')
		if irexpr.type:
			self.dispatch(irexpr.type)
		if irexpr.inst:
			self.write(", ")
			self.dispatch(irexpr.inst)
		if irexpr.tback:
			self.write(", ")
			self.dispatch(irexpr.tback)
		self.write(";")
	
	def _Break(self, irexpr):
		self.write("break")

	def _Continue(self, irexpr):
		self.write("continue")

	def _AssignAttr(self, irexpr):
		'''
		We *may* need to do the whole python attr lookup thing
		call obj.__setattr__ etc
		'''
		self.write("%s.%s = %s" % (irexpr.obj, irexpr.attr, irexpr.value))

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
		self.write('Py_DECREF(%s); %s = NULL' % (irexpr.var, irexpr.var))

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
			self.write(
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
		self.write('%s(%s)' % (irexpr.fn, args))
	
	def _Assign(self, irexpr):
		self.write(repr(irexpr.rhs))

	def _Attr(self, irexpr):
		'''
		same deal as _AssignAttr -- this may need to Python
		'''
		self.write('%s.%s' % (irexpr.obj, irexpr.attr))

	def _Subscript(self, irexpr):
		'''
		same deal as _AssignSubscript
		'''
		self.write("%s[%s]" % (irexpr.obj, irexpr.subscript))


	def _Slice(self, irexpr):
		'''
		same deal as _AssignSlice
		'''
		raise NotImplementedError
	
	def _GetGeneratorSentIn(self, irexpr):
		raise NotImplementedError

	#Get current exception using CPython-C API
	def _GetException(self, irexpr):
		raise NotImplementedError

	#Take IRClass/IRFunction/IRModule and turn them into py objects:
	def _GetModule(self, irexpr):
		raise NotImplementedError

	def _MakeFunction(self, op):
		self.write('P3MakeFunction((fptr)%s_POSCALLER, "%s")' % (op.code.cname, op.code.pyname))

	def _MakeClass(self, irexpr):
		#TODO
		#TOFIX: Classes in C? Not sure I comprehend this...
		#Create Py pipe, It should be a CPython/C API thing
		#For now we'll forget about it
		raise NotImplementedError
