
from BaseTranslator import *

import ast
from IR import *

translatedModules = {}

@translatorSubclass
class ModuleTranslator:
	def __init__(self, modulename, fname):
		self.module = IRModule(modulename)
		translatedModules[fname] = self.module
		
		program.modules.add(self.module)
		program.codes.add(self.module.initcode)
		
		astmodule = parseFile(fname)
		BaseTranslator.__init__(self,
			self.module.initcode.body, 
			astmodule.body
		)

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

def getModuleFile(fname):
	if fname not in translatedModules:
		ModuleTranslator('__main__', fname)
	return translatedModules[fname]


@translatorMixin
class ImportTranslator(object):
	def getModule(self, mname):
		fname = lookupModule(mname)
		return getModuleFile(fname)
		
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


