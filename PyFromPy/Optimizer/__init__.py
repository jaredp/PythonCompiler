import getFunctionTemporaries
import constFlattener
import unreachableCodeRemover
import unusedVariableRemover
import variableUnproxyer
import programPartialEvaluation

def optimize(program):
	programPartialEvaluation.run(program)

	constFlattener.optimize(program)
	unusedVariableRemover.clean(program)
	unreachableCodeRemover.clean(program)

	getFunctionTemporaries.addAnnotationsTo(program)

def correct(program):
	variableUnproxyer.clean(program)
	getFunctionTemporaries.addAnnotationsTo(program)
