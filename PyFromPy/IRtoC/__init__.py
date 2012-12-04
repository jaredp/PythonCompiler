from CTranslator import CTranslator
import sys

def generateProgram(program, out=sys.stdout):
	translator = CTranslator(out)
	translator.generateProgram(program)
