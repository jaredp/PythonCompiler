from base import IRNode
from ir import IRVar
from utils import uniqueID

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

	def __repr__(self):
		return repr(self.members)


class IRFunction(object):
	'''Abstract base class of IRCode and IRBuiltinFunction (stdlib.py)'''
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

	def __init__(self, pyname):
		self.cname = uniqueID(pyname)
		self.pyname = pyname
		
		self.body = []
		self.namespace = Namespace(expandable=False)
		
		# some reasonable defaults
		self.defaults = {}
		self.isgenerator = False


class IRClass(object): __slots__ = [
	'name',			#C name
	'definedname',	#name defined in Python
	#types
]
	
class IRModule(object): 
	__slots__ = [
		'name',
		'docstring',

		'namespace',
		'initcode'		# code block
	]

	def __init__(self, name):
		self.docstring = None
		self.name = name

		self.namespace = Namespace(expandable=True)
		self.initcode = IRCode('load'+name)

		# this both doesn't make sense and doesn't matter
		self.initcode.module = self 


class Program(object):
	codes = set()		# {IRCode}
	classes = set()		# {IRClass}
	modules = set()		# {pyname: IRModule}
	initcode = None		# main module's initcode`


