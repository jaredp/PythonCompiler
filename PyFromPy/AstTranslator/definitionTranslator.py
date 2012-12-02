from IR import *
from BaseTranslator import *

import ast
from utils import matches, __, ___

@translatorSubclass
class FunctionTranslator:
	def __init__(self, pyname, argsast, ast):
		BaseTranslator.__init__(self)

		self.function = IRCode(pyname)
		program.codes.add(self.function)

		#self.function.module = ?

		#args can be Names, Assign([Name], expr), or Tuple
		self.function.args = []
		for argast in argsast:
			if matches(argast, ast.Name):
				argname = argsast.id
				self.function.args.append(argname)

				var = self.getVarNamed(argname)
				self.function.argvars.append(var)

			elif matches(argsast, ast.Assign([ast.Name], __)):
				# we assume the expression was evaluated externally
				argname = argsast.targets[0].id
				self.function.defaults.append(argname)
				self.function.args.append(argname)

				var = self.getVarNamed(argname)
				self.function.argvars.append(var)

			elif matches(argsast, ast.Tuple):
				self.function.args.append(None)
				
				argvar = IRVar()
				self.function.argsvars.append(argvar)
				
				self.makeAssignment(argsast, argvar)

			else:
				self.error("unexpected argument %s" % argsast)

		self.buildBlock(self.function.body, ast)
		self.function.namespace = self.namespace
		self.function.globals = self.getGlobals()
		

@translatorMixin
class Definitions:
	def _FunctionDef(t, name, args, body, decorator_list):
		translator = FunctionTranslator(name, args, body)
		fn = MakeFunction(translator.function, [], [])
		decorated = t.decorate(fn, decorator_list)
		Assign(target=t.getTargetNamed(name), rhs=decorated)

	def decorate(t, obj, decorator_list):
		for decorator_expr in decorator_list:
			decorator = t(decorator_expr)
			obj = FCall(decorator, [obj], [], None, None)
		return obj
	
	def _ClassDef(s, name, bases, body, decorator_list):
		raise NotImplementedError

	def _Lambda(s, args, body):
		raise NotImplementedError
	
	
