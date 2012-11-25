from IR.ir import *
from IR.environments import *

class BuiltinFn(IRFunction):
	def __init__(self, fname, *args):
		self.cname = fname
		self.args = list(args)
		globals()[fname] = self

	def call(this, dest, *args):
		return ConstCall(dest, this, list(args))
	__call__ = call

	def callVoid(this, *args):
		return this(None, *args)
	
	def __repr__(this):
		return this.cname

BuiltinFn('PyPrint', 'dest', 'obj')
BuiltinFn('MyPrint', 'obj')
BuiltinFn('PyPrintNl')

BuiltinFn('MakeTuple', 'size')
BuiltinFn('SetTupleComponent', 'tuple', 'index', 'value')

BuiltinFn('Iter', 'container')
BuiltinFn('Next', 'iterator')

BuiltinFn('Globals')
BuiltinFn('Locals')
