import getFunctionTemporaries
import constFlattener
import unreachableCodeRemover
import unusedVariableRemover

def optimize(program):
	constFlattener.optimize(program)

def correct(program):
	getFunctionTemporaries.addAnnotationsTo(program)
	unusedVariableRemover.clean(program)
