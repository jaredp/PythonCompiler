
from IR import ir
from BaseTranslator import translatorMixin

@translatorMixin
class ControlFlow:
	def _If(s, test, body, orelse):
		return ir.If(
			s.translateExpr(test),
			s.translateBlock(body),
			s.translateBlock(orelse)
		)
	
	def _IfExp(s, test, body, orelse):
		raise NotImplementedError
	
	def _For(s, target, iter, body, orelse):
		raise NotImplementedError
		
	def _While(s, test, body, orelse):
		raise NotImplementedError
		
	def _Pass(s):
		raise NotImplementedError
	
	def _Break(s):
		raise NotImplementedError
	
	def _Continue(s):
		raise NotImplementedError
		
	def _With(s, context_expr, optional_vars, body):
		raise NotImplementedError
	
	def _Return(s, value):
		rettemp = s.translateExpr(value)
		return ir.Return(rettemp)
	
	def _Yield(s, value):
		raise NotImplementedError
	
	def _Raise(s, type, inst, tback):
		raise NotImplementedError
	
	def _TryExcept(s, body, handlers, orelse):
		raise NotImplementedError

	def _TryFinally(s, body, finalbody):
		raise NotImplementedError
	

