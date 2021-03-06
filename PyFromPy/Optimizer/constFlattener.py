
from optutils import *

def optimize(program):
	consts = collectConsts(program)
	inlineConsts(program, consts)

	consts.update(collectConsts(program))
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
			consts[var] = val

	for op in iterOperationsInProgram(program):
		if isinstance(op, MakeFunction) \
		and op.defaults == [] \
		and op.closures == []:
			found(op.target, op.code)
			
		elif isinstance(op, Assign):
			found(op.target, op.rhs)

		elif isinstance(op, GetModule):
			found(op.target, op.module)

	resolvedconsts = {}
	for (const, val) in consts.items():
		while isinstance(val, IRVar):
			val = consts.get(val, None)
		if val: 
			resolvedconsts[const] = val
		
	return resolvedconsts

@powerReduction
def inlineConsts(op, consts):
	if isinstance(op, FCall) and op.fn in consts:
			'''
			Handling keyword arguments and defaults should happen here, to great effect
			Actually there's a potential bug here with reloading modules + 'global' defaults
			Handling variable arguments should also happen.
			For now, we're just assuming it's only args are positional, and that it
			has all of its args.  This makes the power reduction less powerful, but
			it's what we're using it for anyway.
			'''
			return ConstCall(op.target, consts[op.fn], op.args)
		
	elif isinstance(op, Attr) and op.obj in consts:
			mod = consts[op.obj]
			if isinstance(mod, IRModule):
				return Assign(op.target, mod.getGlobalVar(op.attr))
		
