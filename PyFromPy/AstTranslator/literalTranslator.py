
from IR import *
from BaseTranslator import translatorMixin
from utils import numbered

@translatorMixin
class Literals:
	def _Num(s, n):
		if isinstance(n, int):
			return IRIntLiteral(n)
		else:
			return IRFloatLiteral(n)
		
	def _Str(this, s):
		return IRStringLiteral(s)
		
	def _List(t, elts, ctx):
		s = stdlib.NewList(IRIntLiteral(len(elts)))
		for elt in elts:
			stdlib.ListAppend(s, t(elt))
		return s

	def _Tuple(t, elts, ctx):
		tup = stdlib.MakeTuple(IRIntLiteral(len(elts)))
		for (i, elt) in numbered(elts):
			stdlib.SetTupleComponent(tup, IRIntLiteral(i), t(elt))
		return tup
	
	def _Set(t, elts):
		s = stdlib.NewSet(IRIntLiteral(len(elts)))
		for elt in elts:
			stdlib.SetAdd(s, t(elt))
		return s
	
	def _Dict(t, keys, values):
		size = len(keys)
		assert size == len(values)

		d = stdlib.NewDict(IRIntLiteral(size))
		for (key, value) in zip(keys, values):
			stdlib.DictSet(d, t(key), t(value))
		return d

	
