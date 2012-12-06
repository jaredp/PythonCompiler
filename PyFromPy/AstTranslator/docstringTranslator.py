from IR import *
from BaseTranslator import *

import ast
from utils import matches, __, ___

@translatorMixin
class DocstringTranslator:
	def pullDocstring(s, astcode):
		if matches(astcode, [ast.Expr(ast.Str), ___]):
			s.docstring = astcode.pop(0).value.s
		else:
			s.docstring = None

