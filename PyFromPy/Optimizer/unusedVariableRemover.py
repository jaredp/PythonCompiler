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

