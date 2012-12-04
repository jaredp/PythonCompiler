
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
			loop = Loop([])
			with IRBlock(loop.body):
				elem = stdlib.Next(i)
				If(stdlib.IsStopIterationSignal(elem), [
					Break(noemit=True)
				], [])
				t.makeAssignment(target, elem)
				t.translateStmts(body) 
			
		else:
			# this is depressingly involved
			raise NotImplementedError
		
	def _While(t, test, body, orelse):
		if orelse == []:
			loop = Loop([], noemit=True)
			with IRBlock(loop.body):
				condition = t(test)
				If(stdlib.NotUnaryOp(condition), [
					Break(noemit=True)
				], [])
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
		if value:
			return Return(t(value))
		else:
			return Return(NoneLiteral())
	
	def _Yield(t, value):
		return Yield(t(value))
	
	def _Raise(t, type, inst, tback):
		if inst or tback:
			# I think this is an old form or something...?
			raise NotImplementedError

		return Raise(t(type))

	'''
	Untested.  Currently, it looks like there should be a manual handling
	of the exception stack, where 
	RaiseEx() pushes, Handle() pulls, GetException() gets, and Raise() throws
	'''
	
	def _TryExcept(t, body, handlers, orelse):
		'''
		was going to nest handlers, but that doesn't seem like a good idea
		because a handler can throw and we don't want another to catch it
		''' 
		#exceptioned = IRVar()
		raise NotImplementedError

	def _TryFinally(t, body, finalbody):
		ex = IRVar()
		Assign(target=ex, rhs=IRNoneLiteral())
		_try = Try(
			t.translateBlock(body), 
		None, [
			Assign(target=ex, rhs=GetException(noemit=True))
		])
		t.translateStmts(finalbody)
		If(ex, [Raise(ex, noemit=True)], [])

	

