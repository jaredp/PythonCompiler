from IR.ir import *
from IR.environments import *

class BuiltinFn(IRFunction):
	def __init__(self, fname, *args):
		self.cname = fname
		self.pyname = '`unnamed function`'
		self.docstring = None
		self.module = '__builtin__'
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
BuiltinFn('IsStopIterationSignal', 'nextret')

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

class BinaryOp(BuiltinFn):
	def __init__(self, name):
		BuiltinFn.__init__(self, name, 'lhs', 'rhs')

BinaryOp('AddBinaryOp')
BinaryOp('SubBinaryOp')
BinaryOp('MultBinaryOp')
BinaryOp('DivBinaryOp')
BinaryOp('ModBinaryOp')
BinaryOp('PowBinaryOp')
BinaryOp('LShiftBinaryOp')
BinaryOp('RShiftBinaryOp')
BinaryOp('BitOrBinaryOp')
BinaryOp('BitXorBinaryOp')
BinaryOp('BitAndBinaryOp')
BinaryOp('FloorDivBinaryOp')

BinaryOp('AugAddBinaryOp')
BinaryOp('AugSubBinaryOp')
BinaryOp('AugMultBinaryOp')
BinaryOp('AugDivBinaryOp')
BinaryOp('AugModBinaryOp')
BinaryOp('AugPowBinaryOp')
BinaryOp('AugLShiftBinaryOp')
BinaryOp('AugRShiftBinaryOp')
BinaryOp('AugBitOrBinaryOp')
BinaryOp('AugBitXorBinaryOp')
BinaryOp('AugBitAndBinaryOp')
BinaryOp('AugFloorDivBinaryOp')

BinaryOp('EqCmpOp')
BinaryOp('NotEqCmpOp')
BinaryOp('LtCmpOp')
BinaryOp('LtECmpOp')
BinaryOp('GtCmpOp')
BinaryOp('GtECmpOp')
BinaryOp('IsCmpOp')
BinaryOp('IsNotCmpOp')
BinaryOp('InCmpOp')
BinaryOp('NotInCmpOp')

class UnaryOp(BuiltinFn):
	def __init__(self, name):
		BuiltinFn.__init__(self, name, 'operand')

UnaryOp('InvertUnaryOp')
UnaryOp('NotUnaryOp')
UnaryOp('UAddUnaryOp')
UnaryOp('USubUnaryOp')
