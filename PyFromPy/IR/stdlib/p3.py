from stdbase import *

def BuiltinFn(fname, *args, **kwargs):
	fn = P3CFunction(fname, '`unnamed function`', *args, **kwargs)
	fn.module = '__builtin__'
	globals()[fname] = fn

BuiltinException('StopIterationException')

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

BuiltinFn('NewList')
BuiltinFn('ListAppend', 'member')

BuiltinFn('NewSet', 'size')
BuiltinFn('SetAdd', 'member')

BuiltinFn('NewDict', 'size')
BuiltinFn('DictSet', 'dict', 'key', 'value')

def BinaryOp(fname):
	BuiltinFn(fname, 'lhs', 'rhs')

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

def UnaryOp(fname):
	BuiltinFn(fname, 'operand')

UnaryOp('InvertUnaryOp')
UnaryOp('NotUnaryOp')
UnaryOp('UAddUnaryOp')
UnaryOp('USubUnaryOp')
