from base import IRNode
from ir import IRVar

class Namespace(object):
	__slots__ = [
		'members',			# {pyname -> IRVar}
		'temporaries',		# set(IRVar)
		'isExpandable',		# bool
	]
	
	def __init__(self, expandable=False):
		self.members = {}
		self.temporaries = set()
		self.isExpandable = expandable

	def get(ns, pyname):
		if pyname not in ns.members:
			ns.members[pyname] = IRVar(pyname)
		return ns.members[pyname]

	def newTemporary(self):
		#FIXME: be careful how you use this; could be messy on IRVar.merge
		t = IRVar()
		self.temporaries.add(t)
		return t

	
class IRFunction(IRNode):
	__slots__ = [
		'cname',		# C name		
		'args',			# pynames in namespace.members
		'varargs',
		'kwargs',
		
		#types
	]

	def newTemporary(self):
		#FIXME: be careful how you use this; could be messy on IRVar.merge
		t = IRVar()
		self.temporaries.add(t)
		return t

	def getLocal(self, pyname):
		t = self.namespace.get(pyname)
		self.temporaries.add(t)
		return t

class IRCode(IRFunction):
	__slots__ = [
		'pyname',		# name defined in Python
		'module',		# string name of module fn was defined in
		'body',			# codeblock, or None for builtins
		'defaults',		# {pyname: IRVar} ?

		'captures',		# set(IRVar) ?
		'globals',		# set(IRVar) ?
		
		#flags
		'isgenerator',

		'temporaries',	# set(IRVar)
		'namespace',	# locals, globals, captures, defaults
	]

class IRClass(IRNode): __slots__ = [
	'name',			#C name
	'definedname',	#name defined in Python
	#types
]
	
class IRModule(IRNode): __slots__ = [
	'namespace',
	'initcode'		# code block
]

class Program(IRNode): __slots__ = [
	'codes',	# [IRCode]
	'classes',	# [IRClass]
	'modules',	# [IRModule]
	'initcode',	# IRVar to something that should be in codes
]



