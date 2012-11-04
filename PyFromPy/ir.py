
def getAllSlots(cls):
	slots = []
	for superclass in cls.__bases__:
		slots += getAllSlots(superclass)
	
	if hasattr(cls, '__slots__'):
		slots += cls.__slots__
	
	return slots

class IRNode(object):
	def __init__(self, *args, **kwparams):
		if args != ():
			vals = zip(self.slots(), args) + kwparams.items()
		else:
			vals = kwparams.items()
		for (key, val) in vals:
			setattr(self, key, val)
	
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
	
def makeSubclass(superclass, name, components):
	globals()[name] = type(name, (superclass,), {'__slots__':components})

#############################################################
# IRNodes
#############################################################

[makeSubclass(IRNode, newnode, components) for (newnode, components) in {
	'IRAtom': ['name'],
	'IROperation': ['target'],	# type(target) = IRVar
	'IRBlock': [],
	'IREnvironment': ['namespace'],
 }.items()]

# all code blocks are non-None [IROperation|IRBlock]

[makeSubclass(IRBlock, newnode, components) for (newnode, components) in {
	'If': ['condition', 'then', 'orelse'],	# condition is an IRAtom
	'While': ['condition', 'body'],
	'Try': ['body', 'catch', 'finally']
	# type(catch) = None|(exception (pyname), as (pyname), handler (code block))
}.items()]

[makeSubclass(IRAtom, newnode, components) for (newnode, components) in {
	'IRVar': [],
	'IRIgnore': [],	# name may not be set
	'IRStringLiteral': ['value'],
	'IRIntLiteral': ['value'],
	'IRFloatLiteral': ['value'],
}.items()]

[makeSubclass(IROperation, newnode, components) for (newnode, components) in {
	'BinOp': ['lhs', 'rhs'],
	'UnaryOp': ['arg'],

	'FCall': ['fn', 'args', 'kwargs', 'starargs', 'keystarargs'],
									# type(fn) = IRVar
	'ConstCall': ['fn', 'args'],	# type(fn) = IRFunction
	
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
	
	'MakeFunction': ['code', 'defaults', 'closures'],
	'MakeClass': ['name', 'superclasses']
}.items()]

[makeSubclass(FCall, newnode, components) for (newnode, components) in {
	'MethodCall': ['object']
 }.items()]

[makeSubclass(Setter, newnode, components) for (newnode, components) in {
	'AttrSetter': ['attr'],
	'SubscriptSetter': ['slice']
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

[makeSubclass(object, newnode, components) for (newnode, components) in {
	'Namespace': [
		'slots',			# {pyname -> IRVar}
		'isexpandable',		# bool
		'consts',			# [pyname]
	]
}.items()]

[makeSubclass(IREnvironment, newnode, components) for (newnode, components) in {
	'IRFunction': [
		'name', 'definedname',
		'body',
		
		'args',
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
		'name', 'definedname',
		#types
	],
	
	'IRModule': [
		'functions', 'classes',
		'loadfn'
	],
}.items()]

if __name__ == '__main__':
	print IRVar(name='$1')
	print IRFunction(namespace=Namespace(), name='myFibFn')
	print BinOp('a', 'b', 'c')
	
