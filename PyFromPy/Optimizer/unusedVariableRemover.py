from optutils import *
import getFunctionTemporaries

def clean(program):
	unreadwrites = True
	while unreadwrites:
		readvars, writtenvars = getVarReadWrites(program)
		unreadwrites = writtenvars - readvars
		ignoreWritesTo(program, unreadwrites)
		removeNoOps(program)

	#unwrittenreads = readvars - writtenvars
	'''
	FIXME: we should be replacing anything that
	uses an unwrittenread with a raise, but that
	shouldn't happen in a real program, and I don't
	have the raise mechanism properly yet
	'''

def getVarReadWrites(program):
	readvars, writtenvars = set(), set()
	for op in iterOperationsInProgram(program):
		writtenvars.add(getTarget(op))
		for operand in getOperands(op):
			readvars.add(operand)
	return readvars, writtenvars - {None}

@operationTransformation
def removeNoOps(op):
	return [] if (not hasSideEffects(op) and getTarget(op) == None) else [op]

def hasSideEffects(op):
	'''
	Side effects are considered to mean any effect on program state
	other than production of the return value. 

	The following almost all have specializations which don't have
	side effects, but these are hard to analyze.

	ConstCalls, for example, may or may not be pure depending on their
	fn's bodies.  This analysis is involved, and will be done later.
	We should be able to check pureness of ConstCalls to BuiltinFunctions
	by looking up an annotation on the BuiltinFunction, but these have
	not been done yet, and should be done with stdlib restructuring in v0.3

	Attr should not have side effects, but must be able to fall back to
	__getattr__.  Ideally, we'd know the type of the object, and be able
	to look up if an attr access would have side effects.
	'''
	return not isinstance(op, IRProducingOp) or type(op) in [
		FCall, MethodCall, ConstCall,
		Attr,
	]