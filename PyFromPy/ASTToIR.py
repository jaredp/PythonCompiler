from utils import *

import ast
from ast import *

import ir
from ir import *

from stdlibdefs import *
from irutils import *

def translate(astmodule):
	return Translator(astmodule).module

class Environment(object):
	pass

class Translator(object):
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
	
	
	#############################################################
	# Statement -> IROperation|IRBlock
	#############################################################
	
	def _Global(s, names):
		if s.isInGlobalBlock():
			s.error("global declaration in global scope")
		
		for name in names:
			
			
	
	def _Del(s, targets):
		for target in targets:
			if isinstance(target, ast.Name):
				var = s.getTargetNamed(target.id)
				s.emit(ir.DeleteVar(var))
				
			elif isinstance(target, ast.Attribute):
				irobj = s.translateExpr(target.value)
				op = ir.DeleteAttr(target=irobj, attr=target.attr)
				
			elif isinstance(target, ast.Subscript):
				pass	# FIXME!
				
			elif type(target) in [ast.List, astTuble]:
				s._Del(target.elts)
	
	def _Return(s, value):
		rettemp = s.translateExpr(value)
		return ir.Return(rettemp)
	
	def _If(s, test, body, orelse):
		return ir.If(
			s.translateExpr(test),
			s.translateBlock(body),
			s.translateBlock(orelse)
		)
	
	def _Assign(s, targets, value):
		rhstemp = s.translateExpr(value)
		return s.makeAssignment(targets, rhstemp)
		
	def makeAssignment(s, asttargets, irrhs):
		unpackAsgns = []
	
		for target in asttargets:
			if isinstance(target, ast.Name):
				irtarget = s.getTargetNamed(target.id)
				op = ir.Assign(irtarget, irrhs)
				
			elif isinstance(target, ast.Attribute):
				#we're not assigning to the target, so we don't add it to locals
				irobj = s.translateExpr(target.value)
				op = ir.AttrSetter(target=irobj, attr=target.attr, rhs=irrhs)
				
			elif isinstance(target, ast.Subscript):
				pass # FIXME!
			
			elif type(target) in [ast.List, ast.Tuple]:
				unpackAsgns.append(target.elts)
				continue
			
			s.emit(op)
			
		if len(unpackAsgns) > 0:
			#FIXME: wrong error would be thrown on unpacking
			#wrong # of compoents at runtime, I think.  May want to add OP
		
			iterator = s.getNewTemporary()
			s.emit(ir.Iter(target=iterator, arg=irrhs))
			componentCount = len(unpackAsgns[0])
			if not all([len(upa) == componentCount for upa in unpackAsgns]):
				#TODO: make this runtime?
				s.error('too many/not enough values to unpack')
			
			componentsTargets = zip(*unpackAsgns)
			for cAsgn in componentsTargets:
				component = s.getNewTemporary()
				s.emit(ir.Next(target=component, arg=iterator))
				s.makeAssignment(cAsgn, component)

	#############################################################
	# Statement -> IROperation
	#############################################################
	
	def _Print(s, dest, values, nl):
		if dest == None:
			for vAst in values:
				arg = s.translateExpr(vAst)
				s.emit(PrintBuiltin.callVoidOp(arg))
		else:
			destination = translateExpr(dest)
			for vAst in values:
				arg = s.translateExpr(vAst)
				s.emit(PrintBuiltinTo.callVoidOp(destination, arg))
		if nl:
			s.emit(PrintNLBuiltin.callVoidOp())

	def _Assert(s, test, msg):
		pass

	def _Expr(s, value):
		# NOTE: Do not return this; translateExpr emits it
		s.translateExpr(value)


	#############################################################
	# Expr -> IROperation
	#############################################################

	def _Call(s, func, args, keywords, starargs, kwargs):
		return FCall(
			s.getNewTemporary(),
			s.translateExpr(func),
			[s.translateExpr(arg) for arg in args],
			[(kw, s.translateExpr(arg)) for (kw, arg) in keywords],
			s.translateExpr(starargs) if starargs else None,
			s.translateExpr(kwargs) if kwargs else None
		)
		

	#############################################################
	# Expr -> IRArg
	#############################################################

	def _Num(s, n):
		if isinstance(n, int):
			return IRIntLiteral(n)
		else:
			return IRFloatLiteral(n)
		
	def _Name(s, id, ctx):
		#ctx *should* be ignorable
		return s.getVarNamed(id)
		
		
		
		