from IR.ir import *
from IR.environments import *

class BuiltinFn(IRFunction):
	def __init__(self, fname, *args):
		self.cname = fname
		self.args = list(args)
		globals()[fname] = self

	def __call__(this, *args):
		return ConstCall(this, list(args))

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

BuiltinFn('Repr', 'obj')

BuiltinFn('NewList', 'size')
BuiltinFn('ListAppend', 'member')

BuiltinFn('NewSet', 'size')
BuiltinFn('SetAdd', 'member')

BuiltinFn('NewDict', 'size')
BuiltinFn('DictSet', 'dict', 'key', 'value')

class BuiltinException(object):
	'''
	figuring this out would mean figuring out types in the IR
	We're not there yet
	'''
	def __init__(self, ename):
		self.ename = ename
		globals()[ename] = self

	def __repr__(self):
		return self.ename

BuiltinException('StopIterationException')
