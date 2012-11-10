from utils import *

import ast
from ast import *

import ir
from ir import *


def translate(astmodule):
	return Translator(astmodule).module

class Translator(object):
	def __init__(s, astmodule):
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
		s.currentBlock().append(op)
		
	#code generation infastructure
	def buildBlock(s, block, stmts):
		s.enterBlock(block)
		for line in stmts:
			s.translateLine(line)
		s.leaveBlock()
		
	def translateLine(s, aststmt):
		meth = getattr(s, '_'+aststmt.__class__.__name__)
		aststmt.__dict__.pop('lineno', None) # you may want to track these
		aststmt.__dict__.pop('col_offset', None)
		op = meth(**aststmt.__dict__)
		if isinstance(op, IROperation): s.emit(ir)
	
	def translateExpr(s, astexpr):
		meth = getattr(s, '_'+astexpr.__class__.__name__)
		astexpr.__dict__.pop('lineno', None)
		astexpr.__dict__.pop('col_offset', None)
		op = meth(**astexpr.__dict__)
		if isinstance(op, IROperation):
			s.emit(ir)
			return op.target
		else:	# op is an IRArg
			return op
	
	def translateArg(s, astexpr):
		meth = getattr(s, '_'+astexpr.__class__.__name__)
		astexpr.__dict__.pop('lineno', None)
		astexpr.__dict__.pop('col_offset', None)
		op = meth(**astexpr.__dict__)
		

	
	#############################################################
	# Statement -> IROperation|IRBlock
	#############################################################
	
	def _Assign(s, targets, value):
		rhstemp = s.translateExpr(value)
		return s.makeAssignment(targets, rhstemp)
		
	def makeAssignment(s, asttargets, irrhs):
		unpackAsgns = []
	
		for target in asttargets:
			if isinstance(target, ast.Name):
				irtarget = s.getTargetNamed(target.id)
				op = ir.PlainSetter(irtarget, irrhs)
				
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
			#wrong # of compoents at runtime, I think
		
			iterator = s.getNewTemporary()
			s.emit(ir.Iter(target=iterator, arg=irrhs))
			componentCount = len(unpackAsgns[0])
			if not all([len(upa) == componentCount for upa in unpackAsgns]):
				#TODO: make this runtime?
				raise 'too many/not enough values to unpack'
			
			componentsTargets = zip(*unpackAsgns)
			for cAsgn in componentsTargets:
				component = s.getNewTemporary()
				s.emit(ir.Next(target=component, arg=iterator))
				s.makeAssignment(cAsgn, component)


	#############################################################
	# Expr -> IROperation
	#############################################################

	def _Num(s, n):
		if isinstance(n, int):
			return IRIntLiteral(n)
		else:
			return IRFloatLiteral(n)
		
	def _Name(s, id, ctx):
		#ctx *should* be ignorable
		return s.getVarNamed(id)
		
		
		
		