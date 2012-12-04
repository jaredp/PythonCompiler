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
	def decorated(program):
		program.codes = [
			transform(fn) or fn
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
