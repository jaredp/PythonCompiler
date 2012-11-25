from utils import *
from IR import *

class UserProgramError(Exception):
	pass

program = Program()

class BaseTranslator(object):
	def __init__(s, astmodule):
		s.linenum = s.colnum = 0

		s.module = IRModule('__main__')
		program.modules.add(s.module)
		program.codes.add(s.module.initcode)

		s.namespace = {}			# pyname -> IRVar
		s.assignedVars = set()		# {pyname}
		s.explicitGlobals = set()	# {pyname}

		s.buildBlock(s.module.initcode.body, astmodule.body)

	def currentModule(s):
		return s.currentModule

	def error(s, errmsg):
		raise UserProgramError(
			'error: %s in %s at %s:%s' %
			(errmsg, s.currentModule(), s.linenum, s.colnum)
		)

	def runtimeError(s, errmsg):
		# this actually isn't the proper sig, but w/e for now
		# also, FIXME, raise or something
		s.error(errmsg)

	def getVarNamed(s, pyname):
		if pyname not in s.namespace:
			s.namespace[pyname] = IRVar(pyname)
		return s.namespace[pyname]
		
	def getTargetNamed(s, pyname):
		s.assignedVars.add(pyname)
		return s.getVarNamed(pyname)
	
	def declareGlobal(s, gbl):
		s.explicitGlobals.add(gbl)
		
	#error handling
	def trackPosition(s, astobj):
		s.linenum = astobj.__dict__.pop('lineno', None)
		s.colnum = astobj.__dict__.pop('col_offset', None)

	def emit(s, op):
		assert isinstance(op, IROperation) or isinstance(op, IRBlock),	\
			"tried to emit %s" % s
		emit(op)
	'''
	def op(s, opclass):
		temp = s.getNewTemporary()
		def maker(*components, **kwcomponents):
			op = opclass(*([temp] + list(components)), **kwcomponents)
			return op
		return maker
	'''		
	#code generation infastructure
	def buildBlock(s, block, stmts):
		enterBlock(block)
		for line in stmts:
			s.translateLine(line)
		leaveBlock()
	
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
	translate = translateExpr

	def _Expr(s, value):
		# NOTE: Do not return this; translateExpr emits it
		s.translateExpr(value)
		
		
translatorMixins = [BaseTranslator]		
def translatorMixin(mixin):
	translatorMixins.append(mixin)
	return mixin
	
def getTranslator():
	return type('Translator', tuple(translatorMixins),  {})
	
		
