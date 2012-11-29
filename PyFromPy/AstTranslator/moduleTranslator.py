
from BaseTranslator import translatorMixin, getTranslator

import ast
from IR import *

def translate(astmodule):
	return Translator(astmodule).module

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

def translateFile(fname):
	return translate(parseFile(fname))

# global becasue a run of the compiler should
# correspond to translating a single entire program
modules = {}

@translatorMixin
class ImportTranslator(object):
	def translateModule(self, mname):
		global modules
		if mname not in modules:
			modfile = lookupModule(mname)
			modules[mname] = translateFile(modfile)
		return modules[mname]
		
	# General FIXME/TODO/UNHANDLED: packages are compeletely unsupported
	def lookupModule(s, mname):
		#FIXME: this is actually fairly complex
		return mname.replace('.', '/') + '.py'
	
	def translateModule(s, mname):
		try:
			return translateFile(s.lookupModule(mname))
		except:
			s.error("no module named %s" % mname)
			
	def _Import(s, names):
		for alias in names:
			asname = alias.asname or alias.name
			target = s.getTargetNamed(asname)
			module = s.translateModule(alias.name)
			s.emit(GetModule(target, module))

	def _ImportFrom(s, module, names, level):
		# no packages -> ignore level
		# TODO: from _ import *
		m = IRVar()
		s.emit(GetModule(m, s.translateModule(module)))

		if len(names) == 1 and names[0].name == '*':
			# from foo import *
			'''
			future strategy:
			import foo as $0
			globals().append($0.__dict___)
			'''
			raise NotImplementedError

		for alias in names:
			asname = s.getTargetNamed(alias.asname or alias.name)
			member = s.getNewTemporary()
			s.emit(Attr(member, m, alias.name))
			s.emit(Assign(asname, member))


Translator = getTranslator()

