
import ast
from ASTToIR import BaseTranslator
from varTranslator import VarTranslator
from controlFlowTranslator import ControlFlowTranslator
from literalTranslator import LiteralTranslator
from operationTranslator import OperationTranslator
from functionTranslator import FunctionTranslator
from generatorTranslator import GeneratorTranslator

def translate(astmodule):
	return Translator(astmodule).module

def parseFile(fname):
	f = open(fname)
	pcode = f.read()
	f.close()
	return ast.parse(pcode, fname)

def translateFile(fname):
	return translate(parseFile(fname))

# General FIXME/TODO/UNHANDLED: packages are compeletely unsupported

def lookupModule(mname):
	#FIXME: this is actually fairly complex
	return mname + '.py'

# global becasue a run of the compiler should
# correspond to translating a single entire program
modules = {}

class ImportTranslator(object):
	def translateModule(self, mname):
		global modules
		if mname not in modules:
			modfile = lookupModule(mname)
			modules[mname] = translateFile(modfile)
		return modules[mname]

	def _Import(s, names):
		for (mname, asname) in names:
			module = translateModule(mname)
			if asname == None:
				asname = mname
			s.emit(GetModule(asname, module))

	def _ImportFrom(s, module, names, level):
		# no packages -> ignore level
		# TODO: from _ import *
		module = translateModule(mname)
		for (name, asname) in names:
			copyop = Assign(
				s.setTargetNamed(asname),
				module.getVarNamed(name)
			)
			s.emit(copyop)


class Translator(BaseTranslator,
	ImportTranslator, 
	VarTranslator, 
	ControlFlowTranslator, 
	LiteralTranslator,
	OperationTranslator,
	FunctionTranslator,
	GeneratorTranslator):
	pass


