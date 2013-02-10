
from BaseTranslator import *

import ast
from IR import *

import os.path as path

project_root = ''
translatedModules = {}

def getRootModuleFile(p):
	global project_root
	project_root, fname = path.split(p)
	return getModuleFile(
		'__main__', 
		open(p), 
		fname
	)

def getModuleFile(mname, f, fname, outer = None):
	pcode = f.read()
	f.close()
	astcode = ast.parse(pcode, fname)

	if fname not in translatedModules:
		#ModuleTranslator puts itself into translatedModules
		ModuleTranslator(outer, mname, fname, astcode)
	return translatedModules[fname]

def getModule(mname, outer):
	try:
		fname = path.join(*([project_root] + mname.split('.'))) + '.py' 
		f = open(fname)
		return getModuleFile(mname, f, fname, outer)
	except IOError:
		if mname in stdlib.modules:
			m = stdlib.modules[mname]
			program.modules.add(m)
			program.codes.add(m.initcode)
			return m
		else:
			raise


@translatorMixin
class ImportTranslator(object):
	def getModule(self, mname):
		try:
			module = getModule(mname, self)
			ConstCall(module.initcode, [])
			return module
		except IOError:
			self.error("no module named %s" % mname)		

	####################################################
	# Importers
	####################################################
	
	def _Import(s, names):
		for alias in names:
			asname = alias.asname or alias.name
			module = s.getModule(alias.name)
			GetModule(module, target=s.getTargetNamed(asname))

	def _ImportFrom(s, module, names, level):
		# no packages -> ignore level
		# TODO: from _ import *
		m = GetModule(s.getModule(module))

		if len(names) == 1 and names[0].name == '*':
			# from foo import *
			'''
			future strategy:
			import foo as $0
			globals().append($0.__dict___)
			'''
			print names
			raise NotImplementedError

		for alias in names:
			as_name = s.getTargetNamed(alias.asname or alias.name)
			Attr(m, alias.name, target=as_name)


@translatorSubclass
class ModuleTranslator:
	def __init__(self, outer, modulename, fname, astmodule):
		BaseTranslator.__init__(self, outer)

		self.module = IRModule(modulename)
		translatedModules[fname] = self.module
		
		program.modules.add(self.module)
		program.codes.add(self.module.initcode)
		
		self.pullDocstring(astmodule.body)
		self.buildBlock(
			self.module.initcode.body, 
			astmodule.body
		)

		with IRBlock(self.module.initcode.body):
			Return(NoneLiteral())

		self.module.docstring = self.docstring
		self.module.namespace = self.namespace

		self.module.initcode.globals = set(self.namespace.keys())
		self.module.initcode.namespace = self.namespace
		# the initcode's namespace IS the global namespace

	def declareGlobal(self, gbl):
		self.error('global declaration illegal in global scope')

	def currentModule(self):
		return self.module