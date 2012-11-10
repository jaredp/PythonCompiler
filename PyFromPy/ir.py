
def getAllSlots(cls):
	slots = []
	for superclass in cls.__bases__:
		slots += getAllSlots(superclass)
	
	if hasattr(cls, '__slots__'):
		slots += cls.__slots__
	
	return slots
	
def makeSubclass(superclass, name, components):
	globals()[name] = type(name, (superclass,), {'__slots__':components})
	
#############################################################
# Basic Nodes
#############################################################

class IRNode(object):
	def __init__(self, *args, **kwparams):
		if args != ():
			vals = zip(self.slots(), args) + kwparams.items()
		else:
			vals = kwparams.items()
		for (key, val) in vals:
			setattr(self, key, val)
	
	isa = isinstance
	
	def slots(self):
		return getAllSlots(self.__class__)
	
	def contents(self):
		return [
			(slot, getattr(self, slot))
			for slot in self.slots()
			if hasattr(self, slot)
		]
	
	def __repr__(self):
		classname = self.__class__.__name__
		attrs = ['%s = %s' % attr for attr in self.contents()]
		attrsRep = ', '.join(attrs)
		return '<%s of %s>' % (classname, attrsRep)

class IRVar(IRNode):
	nextnum = 0
	
	value = None
	# use if there's some kind of constant value, like a class, function, or potentially literal
	
	__slots__ = ['num', 'name', 'value'] # and some type stuff...
	
	def __init__(self, nameSuggestion=''):
		self.num = IRVar.nextnum
		self.name = uniqueID(nameSuggestion)
	
	def __eq__(lhs, rhs):
		return lhs.num == rhs.num
	
	def isActually(lhs, rhs):
		lhs.num = rhs.num
		lhs.name = rhs.name
		#probably something with values/types but that's beyond here
	
	def __repr__(self):
		return self.name

def uniqueID(suggestion=''):
	uid = suggestion+'$'+str(IRVar.nextnum)
	IRVar.nextnum += 1
	return uid

#############################################################
# IRNodes
#############################################################

[makeSubclass(IRNode, newnode, components) for (newnode, components) in {
	'IRArg': [],				# argument to operation
	'IROperation': ['target'],	# type(target) = IRVar|None
	'IRBlock': [],
	'IREnvironment': ['namespace', 'docstring'],
 }.items()]

# all code blocks are non-None [IROperation|IRBlock]

[makeSubclass(IRBlock, newnode, components) for (newnode, components) in {
	'If': ['condition', 'then', 'orelse'],	# condition is an IRAtom
	'While': ['condition', 'body'],
	'Try': ['body', 'catch', 'finally']
	# type(catch) = None|(exception (pyname), as (pyname), handler (code block))
}.items()]

[makeSubclass(IRArg, newnode, components) for (newnode, components) in {
	'IRVarRef': ['var'],# type(var) = IRVar
	'IRStringLiteral': ['value'],
	'IRIntLiteral': ['value'],
	'IRFloatLiteral': ['value'],
}.items()]

[makeSubclass(IROperation, newnode, components) for (newnode, components) in {
	'BinOp': ['lhs', 'rhs'],
	'UnaryOp': ['arg'],

	# type(fn) = IRAtom
	'FCall': ['fn', 'args', 'kwargs', 'starargs', 'keystarargs'],
	
	# type(fn) = IRFunction
	'ConstCall': ['fn', 'args'],
	
	'Subscript': ['slice'],
	'Attr':	['attr'],

	'Setter': ['rhs'],

	#returns/yields/raises target
	'Return': [],
	'Raise': [],
	'Yield': [],
	
	'GetGeneratorSentIn': [],
	'GetLocals': [],
	'GetGlobals': [],
	
	'MakeFunction': ['code', 'defaults', 'closures'],	# type(code) = IRFunction
	'MakeClass': ['name', 'superclasses'],
	
	#these are actually builtin functions...
	'GetType': ['inspected'],		# type(inspected)
	'Iter': ['arg'],
	'Next': ['arg']
}.items()]

[makeSubclass(FCall, newnode, components) for (newnode, components) in {
	'MethodCall': ['object']
 }.items()]

[makeSubclass(Setter, newnode, components) for (newnode, components) in {
	'PlainSetter': [],
	'AttrSetter': ['attr'],
	'SubscriptSetter': ['slice']	# no idea what this is yet / several options
}.items()]

[makeSubclass(BinOp, op, []) for op in [
	'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Pow',
	'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd',
	
	'AugAdd', 'AugSub', 'AugMult', 'AugDiv', 'AugFloorDiv', 'AugMod', 'AugPow',
	'AugLShift', 'AugRShift', 'AugBitOr', 'AugBitXor', 'AugBitAnd',

	'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn',
	
	'And', 'Or'
]]

[makeSubclass(UnaryOp, op, []) for op in [
	'Invert', 'Not', 'UAdd', 'USub'
]]

cpythonFunctions = []	# [IRFunction(del body)]; add to this elsewhere

# pyname is the label for something in python, represented as a string

class Namespace(object):
	__slots__ = [
		'members',			# {pyname -> IRVar}
		'temporaries',		# set(IRVar)
		'isExpandable',		# bool
	]
	
	def __init__(self, expandable=False):
		self.members = {}
		self.temporaries = set()
		self.isExpandable = expandable

	def newTemporary(self):
		#FIXME: be careful how you use this; could be messy on IRVar.merge
	
		t = IRVar()
		self.temporaries.add(t)
		return t

[makeSubclass(IREnvironment, newnode, components) for (newnode, components) in {
	'IRFunction': [
		'name',			#C name
		'definedname',	#name defined in Python
		'body',
		
		'args',		# pynames in namespace.members
		'varargs',
		'kwargs',
				   
		'defaults',	# IRVars?
		'captures',	# IRVars?
		'globals',
		
		#flags
		'isgenerator',
		
		#types
	],
	
	'IRClass': [
		'name',			#C name
		'definedname',	#name defined in Python
		#types
	],
	
	'IRModule': [
		'functions',	# [IRFunction]
		'classes',		# [IRClass]
		'toplevel'		# code block
	],
}.items()]


code_print_indentation_lvl = 0
def _print_indented(s):
	print '  '*code_print_indentation_lvl + s

def pprintCodeBlock(codeblock):
	for op in codeblock:
		op.pprint()

def _pprintOp(op):
	_print_indented(repr(op))
IROperation.pprint = _pprintOp
	
def _pprintMod(mod):
	print mod.namespace
	print 'functions:', mod.functions
	print 'main:'
	pprintCodeBlock(mod.toplevel)
IRModule.pprint = _pprintMod
	
if __name__ == '__main__':
	print IRVarRef(var=IRVar())
	print IRFunction(namespace=Namespace(), name='myFibFn')
	print BinOp('a', 'b', 'c')
	
