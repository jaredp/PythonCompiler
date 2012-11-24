
from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class Literals:
	def _Num(s, n):
		if isinstance(n, int):
			return IRIntLiteral(n)
		else:
			return IRFloatLiteral(n)
		
	def _Str(this, s):
		raise IRStringLiteral(s)
		
	def _List(s, elts, ctx):
		raise NotImplementedError

	def _Tuple(s, elts, ctx):
		size = len(elts)
		t = s.getNewTemporary()
		s.emit(stdlib.MakeTuple(t, IRIntLiteral(size))
		i = 0
		for elt in elts:
			c = s.translateExpr(elt)
			s.emit(s.op(stdlib.SetTupleComponent)(t, IRIntLiteral(i), c))
			i += 1
		return t.target
	
	def _Set(s, elts):
		raise NotImplementedError
	
	def _Dict(s, keys, values):
		raise NotImplementedError
				
	
