
from IR import *
from BaseTranslator import translatorMixin

@translatorMixin
class Functions:	
	def _Call(t, func, args, keywords, starargs, kwargs):
		#FIXME: if func is an Attr, this is a method
		return FCall(
			t(func),
			[t(arg) for arg in args],
			[(kw, t(arg)) for (kw, arg) in keywords],
			t(starargs) if starargs else None,
			t(kwargs) if kwargs else None
		)
	
		
	def _Print(t, dest, values, nl):
		if dest == None:
			for vAst in values:
				stdlib.MyPrint(t(vAst))

		else:
			destination = t(dest)
			for vAst in values:
				stdlib.PyPrint(destination, t(vAst))

		if nl:
			stdlib.PyPrintNl()


	def _Repr(t, value):
		return stdlib.Repr(t(value))


