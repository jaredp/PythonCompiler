from IR import *

class GetterTranslator:
	def _Name(s, id, ctx):
		#ctx *should* be ignorable
		return s.getVarNamed(id)

	def _Attribute(s, value, attr, ctx):
		raise NotImplementedError
	
	def _Subscript(s, value, slice, ctx):
		raise NotImplementedError

