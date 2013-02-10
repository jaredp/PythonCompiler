from optutils import *

class ReturnCFE(Exception): pass
class RaiseCFE(Exception): pass # not sure we're doing exceptions
# not doing generators

class BreakCFE(Exception): pass
class ContinueCFE(Exception): pass

class Unknowable: 
	def __init__(self, last_known=None):
		self.last_known = last_known

program = None
state = {}			# {IRVar: value}
all_globals = set() # {IRVar}

def mark_unknowable(var):
	last_known = state.get(gvar, None)
	state[gvar] = Unknowable(last_known)

def is_known(var):
	return var in state and not isinstance(state[var], Unknowable)

def markAllGlobalsUnknowable():
	for gvar in all_globals:
		mark_unknowable(gvar)

interpreters = {}
def interpret(op):
	def decorator(handler):
		interpreters[op] = handler
		return handler
	return decorator

'''
need a way to serialize things?
'''

def knowAllOperands(op):
	return all([is_known(operand) for operand in getOperands(op)])

def runOn(codeblock):
	for op in codeblock:
		opcode = type(op)
		if opcode in interpreters and knowAllOperands(op):
			state[op.target] = interpreters[type(op)](op)

def run(p):
	global program
	global state
	global all_globals

	program = p
	for m in program.modules:
		for (_, gvar) in m.namespace.items():
			all_globals.add(gvar)

	state = {
		stdlib.modules['__builtin__'].namespace['globals']: mockGlobals
	}

	runOn(program.initcode.body)

	program = None
	all_globals = {}
	state = {}


################
# globals()

def get_main_module():
	'''
	this shouldn't be necessary, but mockGlobals just
	picks the main module.  This should look at the current function
	and get its module, but this would require significant rewrites
	'''
	for module in program.modules:
		if module.initcode == program.initcode:
			return module
	return None

def mockGlobals():
	return MockModuleDict(get_main_module())

class MockModuleDict:
	def __init__(self, module):
		self.module = module
	def getitem(self, item):
		return self.module.getGlobalVar(item)
	def setitem(self, item, value):
		gvar = self.module.getGlobalVar(item)
		state[gvar] = value

class MockModule:
	def __init__(self, module):
		self.module = module
	def getattr(self, attr):
		if attr == '__dict__':
			return MockModuleDict(self.module)
		return self.module.getGlobalVar(attr)
	def setattr(self, attr, value):
		if attr == '__dict__':
			raise NotImplementedError
		gvar = self.module.getGlobalVar(attr)
		state[gvar] = value

@interpret(GetModule)
def iGM(op):
	return MockModule(op.module)

@interpret(Assign)
def iAsn(op):
	return state[rhs]

@interpret(Attr)
def iAttr(op):
	return state[op.obj].getattr(op.attr)

