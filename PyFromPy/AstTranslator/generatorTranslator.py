
from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class Generators:
	def _ListComp(s, elt, generators):
		raise NotImplementedError

	def _SetComp(s, elt, generators):
		raise NotImplementedError

	def _DictComp(s, key, value, generators):
		raise NotImplementedError

	def _GeneratorExp(s, elt, generators):
		raise NotImplementedError


