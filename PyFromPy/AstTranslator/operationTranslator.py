import IR
import ast

class OperationTranslator:
	def _BoolOp(s, op, values):
		raise NotImplementedError
		
	def _BinOp(s, left, op, right):
		raise NotImplementedError
				
	def _UnaryOp(s, op, operand):
		raise NotImplementedError
	
	def _Compare(s, left, ops, comparators):
		raise NotImplementedError

