from ast import *
from IR import *

from BaseTranslator import translatorMixin

@translatorMixin
class Operations:
	def _BinOp(t, left, op, right):
		lhs = t(left)
		rhs = t(right)
		ops = {
			Add: stdlib.AddBinaryOp,
			Sub: stdlib.SubBinaryOp,
			Mult: stdlib.MultBinaryOp,
			Div: stdlib.DivBinaryOp,
			Mod: stdlib.ModBinaryOp,
			Pow: stdlib.PowBinaryOp,
			LShift: stdlib.LShiftBinaryOp,
			RShift: stdlib.RShiftBinaryOp,
			BitOr: stdlib.BitOrBinaryOp,
			BitXor: stdlib.BitXorBinaryOp,
			BitAnd: stdlib.BitAndBinaryOp,
			FloorDiv: stdlib.FloorDivBinaryOp
		}
		op = ops[type(op)]
		return op(lhs, rhs)
		
	def _AugAssign(s, target, op, value):
		'''
		FIXME: this reevaluates target, which is VERY WRONG
		If target has side effects, they get evaluated before
		and after the AugAssign
		'''
		lhs = t(target)

		rhs = t(right)
		ops = {
			Add: stdlib.AugAddBinaryOp,
			Sub: stdlib.AugSubBinaryOp,
			Mult: stdlib.AugMultBinaryOp,
			Div: stdlib.AugDivBinaryOp,
			Mod: stdlib.AugModBinaryOp,
			Pow: stdlib.AugPowBinaryOp,
			LShift: stdlib.AugLShiftBinaryOp,
			RShift: stdlib.AugRShiftBinaryOp,
			BitOr: stdlib.AugBitOrBinaryOp,
			BitXor: stdlib.AugBitXorBinaryOp,
			BitAnd: stdlib.AugBitAndBinaryOp,
			FloorDiv: stdlib.AugFloorDivBinaryOp
		}
		res = ops[type(op)](lhs, rhs)
		t.makeAssignment(target, res)

	def _BoolOp(s, op, values):
		raise NotImplementedError

	def _UnaryOp(s, op, operand):
		raise NotImplementedError
	
	def _Compare(s, left, ops, comparators):
		raise NotImplementedError

