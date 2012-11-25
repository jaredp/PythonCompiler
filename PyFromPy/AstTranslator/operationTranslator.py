import IR
import ast

from BaseTranslator import translatorMixin

@translatorMixin
class Operations:
	def _BoolOp(s, op, values):
		raise NotImplementedError
		
	def _AugAssign(s, target, op, value):
		raise NotImplementedError

	def _BinOp(s, left, op, right):
		raise NotImplementedError
				
	def _UnaryOp(s, op, operand):
		raise NotImplementedError
	
	def _Compare(s, left, ops, comparators):
		raise NotImplementedError

