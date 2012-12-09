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
		if isinstance(line, IROperation):
			yield line

		elif isinstance(line, If):
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

		else:
			raise Exception("invalid ir")

def iterOperationsInProgram(program):
	for fn in program.codes:
		for op in iterOperations(fn.body):
			yield op

def mapTransformToAllOps(transform, op):
	if isinstance(op, IROperation):
		return transform(op)
		
	elif isinstance(op, If):
		return If (
			transform(op.condition),
			powerReduceCodeBlock(op.then, transform),
			powerReduceCodeBlock(op.orelse, transform)
		)

	elif isinstance(op, Loop):
		return Loop (
			powerReduceCodeBlock(op.body, transform)
		)
		
	elif isinstance(op, Try):	#FIXME: I'm not too sure about this one
		return Try (
			powerReduceCodeBlock(op.body, transform),
			powerReduceCodeBlock(op.handler, transform)
		)

def powerReduceCodeBlock(codeblock, transform):
	return [mapTransformToAllOps(transform, op) for op in codeblock]
	
def powerReduction(transform):
	@perFunction
	def decorated(function, *args, **kwargs):
		tf = lambda op: transform(op, *args, **kwargs) or op
		function.body = powerReduceCodeBlock(function.body, tf)
	return decorated




