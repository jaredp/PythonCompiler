
from BaseTranslator import UserProgramError, program, buildTranslators
import controlFlowTranslator
import definitionTranslator
import functionTranslator
import generatorTranslator
import literalTranslator
import operationTranslator
import unimplementedTranslator
import varTranslator
import moduleTranslator

buildTranslators()

def translateFile(fname):
	main_module = moduleTranslator.getModuleFile(fname)
	program.initcode = main_module.initcode
	return program
