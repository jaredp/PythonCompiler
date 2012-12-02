from IR import *
import sys
import cStringIO
import os

class CTRanslator(object):

	def __init__(self, tree, file = sys.stdout):
		self.f = file
		self.future_imports = []
		self._indent = 0
		self.dispatch(tree)
		self.f.write("")
		self.f.flush()

	def generateC(mod):
		file = sys.stdout
		for irop in mod.body:
			cexpr = translateExpr(irop)

	def fill(self, text = ""):
		"Indent a piece of text, according to the current indentation level"
		self.f.write("\n"+"	"*self._indent + text)

	def write(self, text):
		"Append a piece of text to the current line."
		self.f.write(text)

	def enter(self):
		"Print ':', and increase the indentation."
		self.write(":")
		self._indent += 1

	def leave(self):
		"Decrease the indentation level."
		self._indent -= 1

	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		if isinstance(tree, list):
			for t in tree:
				self.dispatch(t)
			return
		attr = "_"+tree.__class__.__name__
		if hasattr(self, attr):
			meth = getattr(self, attr)
			meth(tree)
		else:
			self.write(repr(attr))

	def translateExpr(s, irexpr):
		meth = getattr(s, '_'+irexpr.__class__.__name__)
		return meth(irexpr)

	############### C Translating methods ##################
	# There should be one method per concrete grammar type #
	# Constructors should be grouped by sum type. Ideally, #
	# this would follow the order in the grammar, but	   #
	# currently doesn't.								   #
	########################################################

	def _If(self, irexpr):
		#TODO
		self.fill("if ")
		self.dispatch(irexpr.condition)
		self.enter()
		self.dispatch(irexpr.then)
		self.leave()
		# collapse nested ifs into equivalent elifs.
		#TOFIX: Nested if's not handled properly
		while (irexpr.orelse and len(irexpr.orelse) == 1 and
			   isinstance(irexpr.orelse[0], ir.If)):
			irexpr = irexpr.orelse[0]
			self.fill("else if ")
			self.dispatch(irexpr.condition)
			self.enter()
			self.dispatch(irexpr.then)
			self.leave()
		# final else
		if t.orelse:
			self.fill("else")
			self.enter()
			self.dispatch(irexpr.orelse)
			self.leave()

	def _Loop(self, irexpr):
		#TODO
		#TOFIX: Do we not have different classes for different loop types?
		pass

	def _Try(self, irexpr):
		#TODO
		#TOFIX: What's our strategy for exception handling?
		pass

	def _Return(self, irexpr):
		self.fill("return")
		if irexpr.value:
			self.write(" ")
			self.dispatch(t.value)
		self.write(";")

	def _Yield(self, irexpr):
		self.write("(")
		self.write("yield")
		if irexpr.value:
			self.write(" ")
			self.dispatch(irexpr.value)
		self.write(")")
		self.write(";")

	def _Raise(self, irexpr):
		self.fill('raise ')
		if irexpr.type:
			self.dispatch(irexpr.type)
		if irexpr.inst:
			self.write(", ")
			self.dispatch(irexpr.inst)
		if irexpr.tback:
			self.write(", ")
			self.dispatch(t.tback)
		self.write(";")
	
	def _Break(self, irexpr):
		self.fill("break")
		self.write(";")

	def _Continue(self, irexpr):
		self.fill("continue")
		self.write(";")

	def _AssignAttr(self, irexpr):
		self.fill()
		self.dispatch(irexpr.obj)
		self.write(".")
		self.dispatch(irexpr.attr)
		self.write(" = ")
		self.dispatch(irexpr.value)
		self.write(";")

	def _AssignSubscript(self, irexpr):
		self.fill()
		self.dispatch(irexpr.obj)
		self.write(".")
		self.dispatch(irexpr.subscript)
		self.write(" = ")
		self.dispatch(irexpr.value)
		self.write(";")

	def _AssignSlice(self, irexpr):
		#TODO
		pass
	
	def _DeleteVar(self, irexpr):
		self.write("delete" + " ")
		self.dispatch(irexpr.var)
		self.write(";")

	def _DeleteAttr(self, irexpr):
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

	def _MethodCall(self, irexpr):
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
		pass
	
	def _Assign(self, irexpr):
		self.fill()
		self.dispatch(irexpr.target)
		self.write(" = ")
		self.dispatch(irexpr.rhs)
		self.write(";")

	def _Attr(self, irexpr):
		self.dispatch(irexpr.obj)
		# Special case: 3.__abs__() is a syntax error, so if t.value
		# is an integer literal then we need to either parenthesize
		# it or add an extra space to get 3 .__abs__().
		#if isinstance(irexpr.obj, ir.Num) and isinstance(t.obj.n, int):
		#	self.write(" ")
		self.write(".")
		self.write(irexpr.attr)

	def _Subscript(self, irexpr):
		self.dispatch(irexpr.obj)
		self.write("[")
		self.dispatch(irexpr.subscript)
		self.write("]")
		self.write(";")

	def _Slice(self, irexpr):
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

	def _GetException(self, irexpr):
		#TODO
		pass

	def _GetLocals(self, irexpr):
		#TODO
		pass

	def _GetGlobals(self, irexpr):
		#TODO
		pass
	
	def _GetModule(self, irexpr):
		#TODO
		pass

	def _MakeFunction(self, irexpr):
		#TODO
		pass

	def _MakeClass(self, irexpr):
		#TODO
		#TOFIX: Classes in C? Not sure I comprehend this...
		pass
