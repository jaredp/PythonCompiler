from base import IRNode
from ir import IRVar
from utils import uniqueID


def namespace_getVar(namespace, varname):
	if varname not in namespace:
		namespace[varname] = IRVar(varname)
	return namespace[varname]


class IRFunction(object):
	'''Abstract base class of IRCode and IRBuiltinFunction (stdlib.py)'''
	__slots__ = [
		'pyname',		# name defined in Python
		'cname',		# C name		

		'args',			# pynames in namespace.members|None
		'varargs',
		'kwargs',

		'docstring',
		'module',		# string name of module fn was defined in

		#types
	]

class IRCode(IRFunction):
	__slots__ = [
		'body',			# codeblock, or None for builtins
		'argvars', 		# [IRVar]
		'defaults',		# [pyname] ?

		'globals',		# set(pyname) ?
		'locals',		# set(pyname)
		'temporaries',	# set(IRVar)
		'namespace',	# {pyname -> IRVar}
						# locals, args, globals, captures, defaults
	]

	def __init__(self, pyname):
		self.cname = uniqueID(pyname)
		self.pyname = pyname
		
		self.body = []
		self.namespace = {}
		
		# some reasonable defaults
		self.globals = set()
		self.locals = set()
		self.temporaries = set()

		self.defaults = []
		self.args = []
		self.argvars = []
		self.varargs = None
		self.kwargs = None
		

class IRClass(object): __slots__ = [
	'name',			#C name
	'definedname',	#name defined in Python
	'namespace' 	
	#types
]
	
class IRModule(object): 
	__slots__ = [
		'name',
		'cname',
		'docstring',

		'namespace',	# {pyname -> IRVar}
		'initcode'		# code block
	]

	def __init__(self, name):
		self.docstring = None
		self.name = name
		self.cname = uniqueID(name+'module')

		self.namespace = {}
		self.initcode = IRCode('load'+name)
		self.initcode.args = []
		

		# this both doesn't make sense and doesn't matter
		self.initcode.module = self 

	def getGlobalVar(self, varname):
		return namespace_getVar(self.namespace, varname)


class Program(object):
	def __init__(self):
		self.codes = set()		# {IRCode}
		self.classes = set()	# {IRClass}
		self.modules = set()	# {IRModule}
		self.initcode = None	# main module's initcode



