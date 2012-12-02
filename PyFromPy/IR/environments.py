from base import IRNode
from ir import IRVar
from utils import uniqueID

class Namespace(object):
	__slots__ = [
		'members',			# {pyname -> IRVar}
		'isExpandable',		# bool
	]
	
	def __init__(self, expandable=False):
		self.members = {}
		self.isExpandable = expandable

	def get(ns, pyname):
		if pyname not in ns.members:
			ns.members[pyname] = IRVar(pyname)
		return ns.members[pyname]

	def add(self, members):
		self.members.update(members)

	def __repr__(self):
		return repr(self.members)


class IRFunction(object):
	'''Abstract base class of IRCode and IRBuiltinFunction (stdlib.py)'''
	__slots__ = [
		'cname',		# C name		
		'args',			# pynames in namespace.members|None
		'varargs',
		'kwargs',
		
		#types
	]

class IRCode(IRFunction):
	__slots__ = [
		'pyname',		# name defined in Python
		'module',		# string name of module fn was defined in

		'body',			# codeblock, or None for builtins
		'argvars' 		# [IRVar]
		'defaults',		# [pyname] ?

		'globals',		# set(IRVar) ?
		'temporaries',	# set(IRVar)
		'namespace',	# {pyname -> IRVar}
						# locals, args, globals, captures, defaults
	]

	def __init__(self, pyname):
		self.cname = uniqueID(pyname)
		self.pyname = pyname
		
		self.body = []
		self.namespace = Namespace(expandable=False)
		
		# some reasonable defaults
		self.defaults = []
		self.args = []
		self.argvars = []
		self.varargs = None
		self.kwargs = None
		

class IRClass(object): __slots__ = [
	'name',			#C name
	'definedname',	#name defined in Python
	#types
]
	
class IRModule(object): 
	__slots__ = [
		'name',
		'docstring',

		'namespace',	# {pyname -> IRVar}
		'initcode'		# code block
	]

	def __init__(self, name):
		self.docstring = None
		self.name = name

		self.namespace = Namespace(expandable=True)
		self.initcode = IRCode('load'+name)
		self.initcode.args = []
		

		# this both doesn't make sense and doesn't matter
		self.initcode.module = self 


class Program(object):
	def __init__(self):
		self.codes = set()		# {IRCode}
		self.classes = set()	# {IRClass}
		self.modules = set()	# {IRModule}
		self.initcode = None	# main module's initcode



