
from BaseTranslator import translatorMixin, getTranslator

import ast

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
		return mname + '.py'
	
	def translateModule(s, mname):
		try:
			return translateFile(s.lookupModule(mname))
		except:
			s.error("no module named %s" % mname)
			
	def _Import(s, names):
		for (mname, asname) in names:
			module = s.translateModule(mname)
			if asname == None:
				asname = mname
			s.emit(GetModule(asname, module))

	def _ImportFrom(s, module, names, level):
		# no packages -> ignore level
		# TODO: from _ import *
		module = s.translateModule(module)
		for (name, asname) in names:
			copyop = Assign(
				s.setTargetNamed(asname),
				module.getVarNamed(name)
			)
			s.emit(copyop)

import controlFlowTranslator
import definitionTranslator
import functionTranslator
import generatorTranslator
import literalTranslator
import operationTranslator
import unimplementedTranslator
import varTranslator

Translator = getTranslator()

