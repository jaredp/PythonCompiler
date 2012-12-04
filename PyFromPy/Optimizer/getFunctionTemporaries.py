from IR import *
from optutils import *

@perFunction
def addAnnotationsTo(function):
	temporaries = getTemporaries(function.body)
	namespaced = set(function.namespace.values())
	function.temporaries = temporaries - namespaced


def getTemporaries(codeblock):
	'''
	We're making the assumption that all temporaries will
	be assigned to
	'''

	temporaries = set()

	for op in iterOperations(codeblock):
		if isinstance(op, IRProducingOp):
			temporaries.add(op.target)

	return temporaries