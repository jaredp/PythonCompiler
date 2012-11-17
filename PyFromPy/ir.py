
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
	'IRArg': [],		# argument to operation
	'IROperation': [],	
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
	# majority of OPs are IRProducingOps, meaning they produce something
	# IRProducing OPs are intended to be like 3-address code
	'IRProducingOp': ['target'],	# type(target) = IRVar|None
	
	'Return': ['value'],
	'Yield': ['value'],
	'Raise': ['exception'],
		
	'AttrSetter': ['attr'],
	'SubscriptSetter': ['slice'],	# no idea what this is yet / several options
	
	'DeleteVar': ['var'],			# IRVar
	#figure these out later
	'DeleteAttr': [],
	'DeleteSlice': [],
}.items()]

[makeSubclass(IRProducingOp, newnode, components) for (newnode, components) in {
	'BinOp': ['lhs', 'rhs'],
	'UnaryOp': ['arg'],

	# type(fn) = IRAtom
	'FCall': ['fn', 'args', 'kwargs', 'starargs', 'keystarargs'],
	'MethodCall': ['object', 'methname', 'args', 'kwargs', 'starargs', 'keystarargs'],

	# type(fn) = IRFunction
	'ConstCall': ['fn', 'args'],
	
	'Subscript': ['slice'],
	'Attr':	['attr'],

	'Assign': ['rhs'],
	
	'GetGeneratorSentIn': [],	# x = yield
	'GetLocals': [],			# locals(), but locals can be assigned
	'GetGlobals': [],			# globals(), but globals can be assigned
	
	'MakeFunction': ['code', 'defaults', 'closures'],	# type(code) = IRFunction
	'MakeClass': ['name', 'superclasses'],
	
	#these are actually builtin functions, but they may be assigned to...
	'GetType': ['inspected'],		# type(inspected)
	'Iter': ['arg'],
	'Next': ['arg']
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
		'cname',		#C name
		'pyname',		#name defined in Python
		'body',			#codeblock, or None for builtins
		
		'args',			# pynames in namespace.members
		'varargs',
		'kwargs',
				   
		'defaults',		# [IRVars] ?
		'captures',		# [IRVars] ?
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
