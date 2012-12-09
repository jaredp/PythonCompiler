from IR import *

'''

So a serious issue here is how to mutate in-place during iteration

'''

def perFunction(transform):
	'''
	Map over program.codes and call transform(fn)
	if it returns something, replace the function with it
	otherwise, put the function back in, because
	it was probably modified
	'''
	def decorated(program, *args, **kwargs):
		program.codes = [
			transform(fn, *args, **kwargs) or fn
			for fn in program.codes 
		]
	return decorated

def iterOperations(codeblock):
	for line in codeblock:
		assert isinstance(line, IRNode)

		if isinstance(line, If):
			for op in iterOperations(line.then):
				yield op
			for op in iterOperations(line.orelse):
				yield op

		elif isinstance(line, Loop):
			for op in iterOperations(line.body):
				yield op

		elif isinstance(line, Try):
			for op in iterOperations(line.body):
				yield op

			for op in iterOperations(line.handler):
				yield op

		yield line

def iterOperationsInProgram(program):
	for fn in program.codes:
		for op in iterOperations(fn.body):
			yield op

def mapTransformToAllOps(transform, op):
	if isinstance(op, IROperation):
		return transform(op)
		
	elif isinstance(op, If):
		return transform(If(
			op.condition,
			powerReduceCodeBlock(op.then, transform),
			powerReduceCodeBlock(op.orelse, transform)
		))

	elif isinstance(op, Loop):
		return transform(Loop(
			powerReduceCodeBlock(op.body, transform)
		))
		
	elif isinstance(op, Try):	#FIXME: I'm not too sure about this one
		return transform(Try(
			powerReduceCodeBlock(op.body, transform),
			op.exception,
			powerReduceCodeBlock(op.handler, transform)
		))

def powerReduceCodeBlock(codeblock, transform):
	newblock = []
	for op in codeblock:
		newops = mapTransformToAllOps(transform, op)
		newblock.extend(newops)
	return newblock
		
def operationTransformation(transform):
	@perFunction
	def decorated(function, *args, **kwargs):
		tf = lambda op: transform(op, *args, **kwargs)
		function.body = powerReduceCodeBlock(function.body, tf)
	return decorated

def powerReduction(transform):
	@operationTransformation
	def decorated(op, *args, **kwargs):
		return [transform(op, *args, **kwargs) or op]
	return decorated


@powerReduction
def ignoreWritesTo(op, vars):
	'''
	def ignoreWritesTo(program, vars)
	nulls writes to any var in vars over program

	power reduction over all operations as op,
	vars is the set of variables to ignore 
	writes to.
	'''
	if isinstance(op, IRProducingOp) and op.target in vars:
			op.target = None


def getTarget(op):
	if isinstance(op, IRProducingOp):
		return op.target
	else:
		return None

def getOperands(op):
	if isinstance(op, MakeFunction):
		for component in op.defaults + op.closures:
			yield component
		return

	elif isinstance(op, (FCall, MethodCall, ConstCall)):
		for arg in op.args:
			yield arg

		if isinstance(op, (FCall, MethodCall)):
			for (kw, arg) in op.kwargs:
				yield arg

	for (slot, value) in op.contents():
		if slot != 'target' and isinstance(value, IRVar):
			yield value

