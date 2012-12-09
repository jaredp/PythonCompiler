from IR import *
from BaseTranslator import *

import ast
from utils import matches, __, ___

@translatorSubclass
class FunctionTranslator:
	def __init__(self, outer, pyname, argsast, bodyast):
		BaseTranslator.__init__(self, outer)

		self.function = IRCode(pyname)
		program.codes.add(self.function)

		self.function.module = self.currentModule()
		self.pullDocstring(bodyast)

		#args can be Names, Assign([Name], expr), or Tuple
		with IRBlock(self.function.body):
			self.function.args = []
			for argast in argsast.args:
				if matches(argast, ast.Name):
					argname = argast.id
					self.function.args.append(argname)

					var = self.getTargetNamed(argname)
					self.function.argvars.append(var)

				elif matches(argast, ast.Assign([ast.Name], __)):
					# we assume the expression was evaluated externally
					argname = argast.targets[0].id
					self.function.defaults.append(argname)
					self.function.args.append(argname)

					var = self.getTargetNamed(argname)
					self.function.argvars.append(var)

				elif matches(argast, ast.Tuple):
					self.function.args.append(None)
					
					argvar = IRVar()
					self.function.argvars.append(argvar)

					self.makeAssignment(argast, argvar)

				else:
					self.error("unexpected argument %s" % argast)


		self.buildBlock(
			self.function.body,
			bodyast
		)
		
		with IRBlock(self.function.body):
			Return(NoneLiteral())

		self.function.docstring = self.docstring
		self.function.namespace = self.namespace
		self.function.globals = self.getGlobals()
		self.function.locals = self.getLocals() - set(self.function.args)
		

@translatorMixin
class Definitions:
	def _FunctionDef(t, name, args, body, decorator_list):
		translator = FunctionTranslator(t, name, args, body)
		fn = translator.function
		for gbl in fn.globals:
			fn.namespace[gbl].isActually(t.getVarNamed(gbl))

		# FIXME: captures, defaults

		fnvar = MakeFunction(fn, [], [])
		decorated = t.decorate(fnvar, decorator_list)
		Assign(target=t.getTargetNamed(name), rhs=decorated)

	def decorate(t, obj, decorator_list):
		for decorator_expr in decorator_list:
			decorator = t(decorator_expr)
			obj = FCall(decorator, [obj], [], None, None)
		return obj
	
	def _ClassDef(t, name, bases, body, decorator_list):
		'''
		This only makes sense where the class is declared at
		a top level.  Even then, reloads might mess it up.
		90% of the time, it should work 90% of the time.
		But when it doesn't, currently it's just wrong.
		'''
		if bases:
			raise NotImplementedError

		translator = ClassTranslator(t, name, body)
		for gbl in translator.getGlobals():
			translator.namespace[gbl].isActually(
				t.getVarNamed(gbl)
			)

		for lcl in translator.getLocals():
			translator.namespace[lcl].isActually(
				translator.klass.getClassVar(lcl)
			)

		klass = MakeClass(translator.klass)
		decorated = t.decorate(klass, decorator_list)
		Assign(target=t.getTargetNamed(name), rhs=decorated)

	def _Lambda(s, args, body):
		raise NotImplementedError
	

@translatorSubclass
class ClassTranslator:
	def __init__(self, outer, name, bodyast):
		BaseTranslator.__init__(self, outer)

		self.klass = IRClass(name)
		self.pullDocstring(bodyast)
		self.translateStmts(bodyast)
	
		self.klass.docstring = self.docstring
