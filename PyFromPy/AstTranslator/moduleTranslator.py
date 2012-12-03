
from BaseTranslator import *

import ast
from IR import *

translatedModules = {}

@translatorSubclass
class ModuleTranslator:
	def __init__(self, outer, modulename, fname):
		BaseTranslator.__init__(self, outer)

		self.module = IRModule(modulename)
		translatedModules[fname] = self.module
		
		program.modules.add(self.module)
		program.codes.add(self.module.initcode)
		
		astcode = parseFile(fname).body

		self.pullDocstring(astcode)
		self.buildBlock(
			self.module.initcode.body, 
			astcode
		)
		
		self.module.docstring = self.docstring
		self.module.namespace = self.namespace

		self.module.initcode.globals = set(self.namespace.keys())
		self.module.initcode.namespace = self.namespace
		# the initcode's namespace IS the global namespace

	def declareGlobal(self, gbl):
		self.error('global declaration illegal in global scope')

	def currentModule(self):
		return self.module

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

def getModuleFile(fname, mname, outer = None):
	if fname not in translatedModules:
		ModuleTranslator(outer, mname, fname)
	return translatedModules[fname]


@translatorMixin
class ImportTranslator(object):
	def getModule(self, mname):
		fname = lookupModule(mname)
		return getModuleFile(fname, mname)
		
	# General FIXME/TODO/UNHANDLED: packages are compeletely unsupported
	def lookupModule(mname):
		try:
			return mname.replace('.', '/') + '.py'
		except:
			s.error("no module named %s" % mname)		
			
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
			raise NotImplementedError

		for alias in names:
			as_name = s.getTargetNamed(alias.asname or alias.name)
			Attr(m, alias.name, target=as_name)


