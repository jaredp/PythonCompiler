from IR import *
import sys
#from ctypes import *	-- WHY WAS THIS HERE?

class CTranslator(object):

	########################################################
	# infastructure
	########################################################

	def __init__(self, file = sys.stdout):
		self.f = file
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
		self.write('{')
		self._indent += 1

	def exitBlock(self):
		self._indent -= 1
		self.fill('}')

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
		#TOFIX: namespace is an IRVAR with a single value, or is value a collection of different values??
		for module in program.modules:
			for var in module.namespace.values():
				self.declare(var.name)

		for function in program.codes:
			self.generateFunction(function)

		#define locals and globals
		#PyObject *a$0;
		#locals: IRCode.temporaries
		#globals: IRModule.namespace.values()

	def generateFunction(self, function):
		args = ', '.join(map(repr, function.argvars))
		self.fill('PyObject *%s(%s) ' % (function.cname, args))

		self.enterBlock()

		lcls = [function.namespace[lcl] for lcl in function.locals]
		for localvar in set(lcls) | function.temporaries:
			self.declare(localvar.name)
		self.fill()

		self.genStmts(function.body)
		self.exitBlock()

		self.fill()

	def declare(self, varname):
		self.fill('PyObject *%s = NULL;' % varname)

	############### C Translating methods ##################
	# There should be one method per concrete grammar type #
	# Constructors should be grouped by sum type. Ideally, #
	# this would follow the order in the grammar, but	   #
	# currently doesn't.								   #
	########################################################

	def _IRVar(self, var):
		self.write(repr(var))

	def _If(self, irexpr):
		#TODO
		self.fill("if (%s) " % irexpr.condition)
		self.genBlock(irexpr.then)
		if irexpr.orelse:
			self.write(" else ")
			self.genBlock(irexpr.orelse)

	def _Loop(self, irexpr):
		self.fill('while (1) ')
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
		self.write(";")

	def _Continue(self, irexpr):
		self.write("continue")
		self.write(";")

	def _AssignAttr(self, irexpr):
		'''
		We *may* need to do the whole python attr lookup thing
		call obj.__setattr__ etc
		'''
		self.write("%s.%s = %s" % (irexpr.obj, irexpr.attr, irexpr.value))

	def _AssignSubscript(self, irexpr):
		'''
		This will almost definitely be a stdlib libary call
		It will likely be removed as an op from the IR
		'''
		self.write("%s[%s] = %s" % (irexpr.obj, irexpr.subscript, irexpr.value))

	def _AssignSlice(self, irexpr):
		#TODO
		pass
	
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

	def _DeleteAttr(self, irexpr):
		'''
		Like _AssignSubscript, this will go away
		''' 
		self.write("delete" + " ")
		self.dispatch(irexpr.obj)
		self.write(".")
		self.dispatch(irexpr.attr)
		self.write(";")

	def _DeleteSubscript(self, irexpr):
		#TODO
		pass

	def _DeleteSlice(self, irexpr):
		#TODO
		pass

	#binop = { "Add":"+", "Sub":"-", "Mult":"*", "Div":"/", "Mod":"%",
	#				"LShift":"<<", "RShift":">>", "BitOr":"|", "BitXor":"^", "BitAnd":"&",
	#				"FloorDiv":"//", "Pow": "**"}

	def _BinOp(self, irexpr):
		'''
		These, especially, will likely become stdlib calls
		'''
		self.write("(")
		self.dispatch(irexpr.lhs)
		self.write(" " + self.op[irexpr.op.__class__.__name__] + " ")
		self.dispatch(irexpr.rhs)
		self.write(")")
		self.write(";")

	unop = {"Invert":"~", "Not": "!", "UAdd":"+", "USub":"-"}
	def _UnaryOp(self, irexpr):
		self.write("(")
		self.write(self.unop[irexpr.op.__class__.__name__])
		self.write(" ")
		# If we're applying unary minus to a number, parenthesize the number.
		# This is necessary: -2147483648 is different from -(2147483648) on
		# a 32-bit machine (the first is an int, the second a long), and
		# -7j is different from -(7j).  (The first has real part 0.0, the second
		# has real part -0.0.)
		if isinstance(irexpr.op, ir.USub) and isinstance(ir.operand, ir.Num):
			self.write("(")
			self.dispatch(irexpr.arg)
			self.write(")")
		else:
			self.dispatch(irexpr.arg)
		self.write(")")
		self.write(";")

	def _FCall(self, irexpr):
		'''
		The function calling mechanism will be among the most
		complex, and in some ways are the focus of this 
		research.  C certainly doesn't have the type of variable
		argument function calling mechanism Python does, so this
		is not a straightforward translation.
		For now, we're going to just call the _ConstCall mechanism.
		'''
		return self._ConstCall(irexpr)

		self.dispatch(irexpr.fn)
		self.write("(")
		comma = False
		for e in irexpr.args:
			if comma: self.write(", ")
			else: comma = True
			self.dispatch(e)
		for e in irexpr.keywords:
			if comma: self.write(", ")
			else: comma = True
			self.dispatch(e)
		if irexpr.starargs:
			if comma: self.write(", ")
			else: comma = True
			self.write("*")
			self.dispatch(irexpr.starargs)
		if irexpr.kwargs:
			if comma: self.write(", ")
			else: comma = True
			self.write("**")
			self.dispatch(irexpr.kwargs)
		
		self.write(")")

	def _MethodCall(self, irexpr):
		'''
		This is the _FCall mechanism, with all the added fun of
		class attribute lookup.  It's entirely possible we wont
		get to classes, and not get to this.
		'''
		self.dispatch(irexpr.fn)
		self.write("(")
		comma = False
		for e in irexpr.args:
			if comma: self.write(", ")
			else: comma = True
			self.dispatch(e)
		for e in irexpr.keywords:
			if comma: self.write(", ")
			else: comma = True
			self.dispatch(e)
		if irexpr.starargs:
			if comma: self.write(", ")
			else: comma = True
			self.write("*")
			self.dispatch(irexpr.starargs)
		if irexpr.kwargs:
			if comma: self.write(", ")
			else: comma = True
			self.write("**")
			self.dispatch(irexpr.kwargs)
		self.write(")")
		self.write(";")

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

		if irexpr.lower:
			self.dispatch(irexpr.start)
		self.write(":")
		if irexpr.end:
			self.dispatch(irexpr.end)
		if irexpr.step:
			self.write(":")
			self.dispatch(irexpr.step)
		self.write(";")
	
	def _GetGeneratorSentIn(self, irexpr):
		#TODO
		pass

	#Get current exception using CPython-C API
	def _GetException(self, irexpr):
		#TODO
		pass

	#Take IRClass/IRFunction/IRModule and turn them into py objects:
	def _GetModule(self, irexpr):
		#TODO
		pass

	def _MakeFunction(self, op):
		self.write('P3MakeFunction(%s, "%s")' % (op.code.cname, op.code.pyname))

		#Treat the function as a function pointer, C does not have nested functions unlike Python
		#PyObject From CPointer irexpr.cname
		#TOFIX: Doublecheck, I've generated the C function pointer, 
		
		#self.write("PyCObject_FromVoidPtr(%s, NULL)" %(irexpr.cname) )
		#self.write(";")

		# we should probably write a C function that does all of this...
		'''
		self.write("PyObject* (*%s)(PyObject*,PyObject*) = %s;" %(irexpr.pyname, irexpr.cname) )
		self.write("PyMethodDef %smethd = {\"function\",%s,METH_VARARGS,\"A new function\"};" %(irexpr.pyname, irexpr.pyname) )
		self.write("PyObject* %sname = PyString_FromString(%smethd.ml_name);" %(irexpr.cname, irexpr.pyname) )
		self.write("PyObject* pyfoo = PyCFunction_NewEx(&%smethd,NULL,name);" %(irexpr.pyname) )
		self.write("Py_DECREF(%sname);" % (irexpr.cname) )
		'''

	def _MakeClass(self, irexpr):
		#TODO
		#TOFIX: Classes in C? Not sure I comprehend this...
		#Create Py pipe, It should be a CPython/C API thing
		#For now we'll forget about it
		pass
