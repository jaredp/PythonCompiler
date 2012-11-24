
from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class Functions:	
	def _Call(s, func, args, keywords, starargs, kwargs):
		return FCall(
			s.getNewTemporary(),
			s.translateExpr(func),
			[s.translateExpr(arg) for arg in args],
			[(kw, s.translateExpr(arg)) for (kw, arg) in keywords],
			s.translateExpr(starargs) if starargs else None,
			s.translateExpr(kwargs) if kwargs else None
		)
	
		
	def _Print(s, dest, values, nl):
		if dest == None:
			for vAst in values:
				arg = s.translateExpr(vAst)
				s.emit(stdlib.MyPrint(None, arg))
		else:
			destination = translateExpr(dest)
			for vAst in values:
				arg = s.translateExpr(vAst)
				s.emit(stdlib.PyPrint(None, destination, arg))
		if nl:
			s.emit(stdlib.PyPrintNl(None))


	def _Repr(s, value):
		raise NotImplementedError


