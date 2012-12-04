
from optutils import *

def optimize(program):
	consts = collectConsts(program)
	inlineConsts(program, consts)

def collectConsts(program):
	'''
	Find specific things that have only been assigned once
	'''
	consts = {}
	def found(var, val):
		if var in consts:
			consts[var] = None
		else:
			consts[]

	@iterOperationsInProgram
	def collect(op):
		if isinstance(op, MakeFunction) \
		and op.defaults == [] \
		and op.captures == []:


	collect(program)

def inlineConsts(program, consts):
	pass
