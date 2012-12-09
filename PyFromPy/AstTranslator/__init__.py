
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
import docstringTranslator

import IREmitter
from BaseTranslator import UserProgramError, program

BaseTranslator.buildTranslators()

def translateFile(fname):
	with IREmitter.autoemit():
		main_module = moduleTranslator.getModuleFile(
			'__main__', 
			open(fname), 
			fname
		)
	program.initcode = main_module.initcode
	return program
