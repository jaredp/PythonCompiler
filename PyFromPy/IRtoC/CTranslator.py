from IR import *
import sys
import cStringIO
import ir
import os

class CTRanslator(object):

	def __init__(self, tree, file = sys.stdout):
		self.f = file
		self.future_imports = []
		self._indent = 0
		self.dispatch(tree)
		self.f.write("")
		self.f.flush()

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

	def generateC(mod):
		file = sys.stdout
		for irop in mod.body:
			cexpr = translateExpr(irop)
			#generate returned code here

	############### C Translating methods ##################
	# There should be one method per concrete grammar type #
	# Constructors should be grouped by sum type. Ideally, #
	# this would follow the order in the grammar, but	   #
	# currently doesn't.								   #
	########################################################

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
		pass

	def _AssignSubscript(self, irexpr):
		pass

	def _AssignSlice(self, irexpr):
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
		pass

	def _DeleteSlice(self, irexpr):
		pass

	binop = { "Add":"+", "Sub":"-", "Mult":"*", "Div":"/", "Mod":"%",
					"LShift":"<<", "RShift":">>", "BitOr":"|", "BitXor":"^", "BitAnd":"&",
					"FloorDiv":"//", "Pow": "**"}

	def _BinOp(self, irexpr):
		self.write("(")
		self.dispatch(irexpr.lhs)
		self.write(" " + self.binop[irexpr.op.__class__.__name__] + " ")
		self.dispatch(irexpr.rhs)
		self.write(")")
		self.write(";")
		#TOFIX: No attribute such as irexpr.op

	unop = {"Invert":"~", "Not": "!", "UAdd":"+", "USub":"-"}
	def _UnaryOp(self, irexpr):
		self.write("(")
		self.write(self.unop[irexpr.op.__class__.__name__])
		self.write(" ")
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

	def _Slice(self, irexpr):
		if irexpr.lower:
			self.dispatch(irexpr.start)
		self.write(":")
		if irexpr.end:
			self.dispatch(irexpr.end)
		if irexpr.step:
			self.write(":")
			self.dispatch(irexpr.step)
	
	def _GetGeneratorSentIn(self, irexpr):
		pass

	def _GetException(self, irexpr):
		pass

	def _GetLocals(self, irexpr):
		pass

	def _GetGlobals(self, irexpr):
		pass
	
	def _GetModule(self, irexpr):
		pass

	def _MakeFunction(self, irexpr):
		pass

	def _MakeClass(self, irexpr):
		#TOFIX: Classes in C? Not sure I comprehend this...
		pass
