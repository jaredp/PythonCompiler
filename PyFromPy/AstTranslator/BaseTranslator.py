from utils import *
from IR import *

class Environment(object):
	def __init__(self, irenv):
		self.ns = irenv
		self.gottenVars = set()
		self.setVars = set()
		self.declaredGlobals = set()


class BaseTranslator(object):
	def __init__(s, astmodule):
		s.linenum = s.colnum = 0
		s.codeBlockStack = []
		s.module = IRModule(
			namespace = Namespace(True),
			docstring = None,
			functions = [],
			classes = [],
			toplevel = [],
		)
		s.environmentStack = []
		s.enterEnvironment(s.module)
		s.buildBlock(s.module.toplevel, astmodule.body)

	#environment stack (namespace)
	def enterEnvironment(s, env):
		# (IREnvironment env, set(string) gottenVars, set(string) locals)
		s.environmentStack.append((env, set(), set()))
	
	def leaveEnvironment(s):
		s.environmentStack.pop()
	
	def currentEnvironment(s):
		return s.environmentStack[-1]
		
	def setDocstring(s, docstring):
		env, _, _ = s.currentEnvironment()
		env.docstring = docstring
		
	#references
	def getVarNamed(s, pyname):
		#FIXME: need to handle captures!
		env, gotten, _ = s.currentEnvironment()
		ns = env.namespace.members
		if pyname in ns:
			var = ns[pyname]
		else:
			var = IRVar(pyname)
			ns[pyname] = var
		gotten.add(pyname)
		return var
		
	def getTargetNamed(s, pyname):
		#if set, will always be local!
		env, _, lcls = s.currentEnvironment()
		ns = env.namespace.members
		if pyname in ns:
			var = ns[pyname]
		else:
			var = IRVar(pyname)
			ns[pyname] = var
		lcls.add(pyname)
		return var

	def getNewTemporary(s):
		env, _, _ = s.currentEnvironment()
		return env.namespace.newTemporary()
	
	def declareGlobal(s):
		pass
		
	#error handling
	def trackPosition(s, astobj):
		s.linenum = astobj.__dict__.pop('lineno', None)
		s.colnum = astobj.__dict__.pop('col_offset', None)

	def error(s, errmsg):
		raise Exception('%s at %s:%s' % (errmsg, s.linenum, s.colnum))

	#code block stack
	def enterBlock(s, block):
		s.codeBlockStack.append(block)
		
	def leaveBlock(s):
		s.codeBlockStack.pop()
		
	def currentBlock(s):
		return s.codeBlockStack[-1]
		
	def isInGlobalBlock(s):
		return currentBlock(s) == s.module.loadfn
		
	def emit(s, op):
		assert isinstance(op, IROperation) or isinstance(op, IRBlock),	\
			"tried to emit %s" % s
			
		s.currentBlock().append(op)
		
	#code generation infastructure
	def buildBlock(s, block, stmts):
		s.enterBlock(block)
		for line in stmts:
			s.translateLine(line)
		s.leaveBlock()
	
	def translateBlock(s, astblock):
		irblock = []
		s.buildBlock(irblock, astblock)
		return irblock
	
	def translateLine(s, aststmt):
		meth = getattr(s, '_'+aststmt.__class__.__name__)
		s.trackPosition(aststmt)
		op = meth(**aststmt.__dict__)
		if op: s.emit(op)
	
	def translateExpr(s, astexpr):
		meth = getattr(s, '_'+astexpr.__class__.__name__)
		s.trackPosition(astexpr)
		op = meth(**astexpr.__dict__)
		if isinstance(op, IROperation):
			s.emit(op)
			return op.target
		else:	# op is an IRArg
			return op

	def _Expr(s, value):
		# NOTE: Do not return this; translateExpr emits it
		s.translateExpr(value)
		
		
translatorMixins = [BaseTranslator]		
def translatorMixin(mixin):
	translatorMixins.append(mixin)
	return mixin
	
def getTranslator():
	return type('Translator', tuple(translatorMixins),  {})
	
		
