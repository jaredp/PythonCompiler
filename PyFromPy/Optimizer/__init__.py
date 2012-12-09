import getFunctionTemporaries
import constFlattener
import unreachableCodeRemover
import unusedVariableRemover
import variableUnproxyer

def optimize(program):
	constFlattener.optimize(program)
	unusedVariableRemover.clean(program)


def correct(program):
	variableUnproxyer.clean(program)
	getFunctionTemporaries.addAnnotationsTo(program)
