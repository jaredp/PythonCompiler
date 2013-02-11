from ast import *
from IR import *

from BaseTranslator import translatorMixin
from IREmitter import *

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

	def _UnaryOp(t, op, operand):
		ops = {
			Invert: stdlib.InvertUnaryOp,
			Not: stdlib.NotUnaryOp,
			UAdd: stdlib.UAddUnaryOp,
			USub: stdlib.USubUnaryOp
		}
		return ops[type(op)](t(operand))
	
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

	def _BoolOp(t, op, values):
		lhs = t(values[0])
		wants_first = isinstance(op, Or)
		t.makeShortCircuitingLogic(wants_first, lhs, values[1:])
		return lhs

	def makeShortCircuitingLogic(t, wants_first, lhs, rhses):
		if rhses == []:
			return

		if wants_first:
			shouldnt_short_circuit = stdlib.InvertUnaryOp(lhs)
		else:
			shouldnt_short_circuit = lhs

		n = If(shouldnt_short_circuit, [], [], noemit=True)
		with IRBlock(n.then):
			Assign(target=lhs, rhs=t(rhses[0]))
			t.makeShortCircuitingLogic(wants_first, lhs, rhses[1:])
		emit(n)




