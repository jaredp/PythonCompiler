
from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class ControlFlow:
	'''
	You may want to create a new Translator for this...
	'''

	def _If(t, test, body, orelse):
		If (t(test),
			t.translateBlock(body),
			t.translateBlock(orelse)
		)
	
	def _IfExp(t, test, body, orelse):
		'''
		if t:
			res = body
		else:
			res = orelse
		return res
		'''
		res = IRVar()

		switch = If(t(test), [], [], noemit=True)

		with IRBlock(switch.then):
			Assign(target=res, rhs=t(body))
		
		with IRBlock(switch.orelse):
			Assign(target=res, rhs=t(orelse))

		emit(switch)
		return res
	
	def _For(t, target, iter, body, orelse):
		'''
		$broke = False
		$i = iter
		try:
			while True:
				target = next($i)
				body
				...break... -> ...broke = True; break...
		except StopIteration:
			pass

		if not $broke:
			orelse
		----
		this can't be efficient with C++ try/catch
		may want to special-case lists
		'''

		if orelse == []:
			i = stdlib.Iter(t(iter))
			loop = Loop([], noemit=True)
			with IRBlock(loop.body):
				try_ = Try([
					# target = next(i)
				], stdlib.StopIterationException, [Break(noemit=True)], noemit=True)
				with IRBlock(try_.body):
					t.makeAssignment(target, stdlib.Next(i))
				emit(try_)

				t.translateStmts(body) 
			emit(loop)
			
			# make that this
			'''
			with Loop():
				with Try as try_:
					t.makeAssignment(target, stdlib.Next(i))
				with try_.handle(stdlib.StopIterationException):
					Break()
				t.translateStmts(body)
			'''
		else:
			# this is depressingly involved
			raise NotImplementedError
		
	def _While(t, test, body, orelse):
		if orelse == []:
			loop = Loop([], noemit=True)
			with IRBlock(loop.body):
				condition = t(test)
				If(condition, [Break(noemit=True)], [])
				t.translateStmts(body)

			emit(loop)

		else:
			raise NotImplementedError
		
	def _Pass(s):
		pass # this is the correct behavior
	
	def _Break(s):
		return Break()
	
	def _Continue(s):
		return Continue()
		
	def _With(t, context_expr, optional_vars, body):
		raise NotImplementedError
	
	def _Return(t, value):
		return Return(t(value))
	
	def _Yield(t, value):
		return Yield(t(value))
	
	def _Raise(t, type, inst, tback):
		if inst or tback:
			# I think this is an old form or something...?
			raise NotImplementedError

		return Raise(t(type))

	def _TryExcept(t, body, handlers, orelse):
		'''
		was going to nest handlers, but that doesn't seem like a good idea
		because a handler can throw and we don't want another to catch it
		''' 
		#exceptioned = IRVar()
		raise NotImplementedError

	def _TryFinally(t, body, finalbody):
		raise NotImplementedError
	

