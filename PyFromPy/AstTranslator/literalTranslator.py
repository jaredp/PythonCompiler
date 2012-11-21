
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
		raise NotImplementedError
		
	def _List(s, elts, ctx):
		raise NotImplementedError

	def _Tuple(s, elts, ctx):
		raise NotImplementedError
	
	def _Set(s, elts):
		raise NotImplementedError
	
	def _Dict(s, keys, values):
		raise NotImplementedError
				
	
