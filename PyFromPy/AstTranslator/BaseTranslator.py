from utils import *
from IR import *
import ast
from utils import matches, ___

class UserProgramError(Exception):
	pass

'''
program is global becasue a run of the compiler should
correspond to translating a single entire program
'''
program = Program()

class BaseTranslator(object):
	def __init__(s):
		s.linenum = s.colnum = 0

		s.namespace = {}			# pyname -> IRVar
		s.assignedVars = set()		# {pyname}
		s.explicitGlobals = set()	# {pyname}

	def pullDocstring(s, astcode):
		if matches(astcode, [ast.Expr(ast.Str), ___]):
			s.docstring = astcode[0].value.s
			astcode = astcode[1:]
		else:
			s.docstring = None


	########################################
	# namespace infastructure
	########################################

	def getVarNamed(s, pyname):
		if pyname not in s.namespace:
			s.namespace[pyname] = IRVar(pyname)
		return s.namespace[pyname]
		
	def getTargetNamed(s, pyname):
		s.assignedVars.add(pyname)
		return s.getVarNamed(pyname)
	
	def declareGlobal(s, gbl):
		s.explicitGlobals.add(gbl)

	########################################
	# namespace interpretation infastructure
	########################################

	def getLocals(self):
		# any variable assigned to not declared global
		return {
			name for name in self.assignedVars
			if name not in self.explicitGlobals
		}
		
	def getGlobals(self):
		return {
			name for name in self.namespace.keys()
			if name not in self.assignedVars 
			or name in self.explicitGlobals
		}

	########################################
	# error handling infastructure
	########################################

	def error(s, errmsg):
		raise UserProgramError(
			'error: %s in %s at %s:%s' %
			(errmsg, s.currentModule(), s.linenum, s.colnum)
		)

	def runtimeError(s, errmsg):
		# this actually isn't the proper sig, but w/e for now
		# also, FIXME, raise or something
		s.error(errmsg)
		
	def trackPosition(s, astobj):
		s.linenum = astobj.__dict__.pop('lineno', None)
		s.colnum = astobj.__dict__.pop('col_offset', None)

	########################################
	# code generation infastructure
	########################################

	def translateStmts(s, stmts):
		for line in stmts:
			s.translateLine(line)

	def buildBlock(s, block, stmts):
		with IRBlock(block):
			s.translateStmts(stmts)
			
	def translateBlock(s, astblock):
		irblock = []
		s.buildBlock(irblock, astblock)
		return irblock
	
	def translateLine(s, aststmt):
		meth = getattr(s, '_'+aststmt.__class__.__name__)
		s.trackPosition(aststmt)
		meth(**aststmt.__dict__)
	
	def translateExpr(s, astexpr):
		meth = getattr(s, '_'+astexpr.__class__.__name__)
		s.trackPosition(astexpr)
		return meth(**astexpr.__dict__)
	__call__ = translate = translateExpr

	def _Expr(s, value):
		# NOTE: Do not return this; translateExpr emits it
		s.translateExpr(value)
		
				
translatorMixins = [BaseTranslator]
def translatorMixin(mixin):
	translatorMixins.append(mixin)
	return mixin

class TranslatorSubclass(object):
	__slots__ = ['mixin', 'subclass']	
	def make(self, *args, **kwargs):
		return self.subclass(*args, **kwargs)
	
translatorSubclasses = set()
def translatorSubclass(mixin):
	sub = TranslatorSubclass()
	sub.mixin = mixin
	sub.subclass = None
	translatorSubclasses.add(sub)
	return sub.make

def buildTranslators():
	global Translator
	Translator = type('Translator', tuple(translatorMixins),  {})
	for s in translatorSubclasses:
		s.subclass = type(
			s.mixin.__name__ + 'Subclass', 
			(s.mixin, Translator),
			{}
		)
	return Translator
	

	
		
