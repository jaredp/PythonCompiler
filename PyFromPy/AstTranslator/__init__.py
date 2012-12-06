
import BaseTranslator
import controlFlowTranslator
import definitionTranslator
import functionTranslator
import generatorTranslator
import literalTranslator
import operationTranslator
import unimplementedTranslator
import varTranslator
import moduleTranslator

import IREmitter
from BaseTranslator import UserProgramError, program

BaseTranslator.buildTranslators()

def translateFile(fname):
	with IREmitter.autoemit():
		main_module = moduleTranslator.getModuleFile(fname, '__main__')
	program.initcode = main_module.initcode
	return program
