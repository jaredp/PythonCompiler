from IR import *
from BaseTranslator import *

@translatorMixin
class Definitions:
	def _FunctionDef(s, name, args, body, decorator_list):
		raise NotImplementedError
	
	def _ClassDef(s, name, bases, body, decorator_list):
		raise NotImplementedError

	def _Lambda(s, args, body):
		raise NotImplementedError
	
	
