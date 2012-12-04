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
		
	def _AugAssign(t, target, op, value):
		lhs = t(target)
		'''
		FIXME: this reevaluates target, which is VERY WRONG
		If target has side effects, they get evaluated before
		and after the AugAssign
		'''

		rhs = t(value)
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

	def _BoolOp(t, op, values):
		raise NotImplementedError

	def _UnaryOp(t, op, operand):
		raise NotImplementedError
	
	def _Compare(t, left, ops, comparators):
		lhs = t(left)
		c_op_switch = {
			Eq: stdlib.EqCmpOp,
			NotEq: stdlib.NotEqCmpOp,
			Lt: stdlib.LtCmpOp,
			LtE: stdlib.LtECmpOp,
			Gt: stdlib.GtCmpOp,
			GtE: stdlib.GtECmpOp,
			Is: stdlib.IsCmpOp,
			IsNot: stdlib.IsNotCmpOp,
			In: stdlib.InCmpOp,
			NotIn: stdlib.NotInCmpOp
		}
		for (c_op, right) in zip(ops, comparators):
			rhs = t(right)
			comparison = c_op_switch[type(c_op)](lhs, rhs)
			'''
			This should actually do some cool looping thing
			but it's late and that's underused
			'''
			return comparison
