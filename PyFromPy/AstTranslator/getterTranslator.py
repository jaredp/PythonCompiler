from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class Getters:
	def _Attribute(s, value, attr, ctx):
		raise NotImplementedError
	
	def _Subscript(s, value, slice, ctx):
		raise NotImplementedError

