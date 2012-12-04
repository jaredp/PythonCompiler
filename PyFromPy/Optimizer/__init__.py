import getFunctionTemporaries
import constFlattener

def optimize(program):
	constFlattener.optimize(program)

def correct(program):
	getFunctionTemporaries.addAnnotationsTo(program)
