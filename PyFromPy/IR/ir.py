
from IR.base import IRNode, IRVar

def _subclass(superclass, subclasses):
	bases = (superclass,)
	for name, components in subclasses.items():
		newclass = type(name, bases, {'__slots__':components})
		globals()[name] = newclass


#############################################################
# IRNodes
#############################################################

_subclass(IRNode, {
	'IRArg': [],		# argument to operation
	'IROperation': [],	
	'IRBlock': [],
	'IREnvironment': ['namespace', 'docstring'],
 })

# all code blocks are non-None [IROperation|IRBlock]

_subclass(IRBlock, {
	'If': ['condition', 'then', 'orelse'],	# condition is an IRAtom
	'While': ['condition', 'body'],
	'Try': ['body', 'catch', 'finally']
	# type(catch) = None|(exception (pyname), as (pyname), handler (code block))
})

_subclass(IRArg, {
	'IRVarRef': ['var'],# type(var) = IRVar
	'IRStringLiteral': ['value'],
	'IRIntLiteral': ['value'],
	'IRFloatLiteral': ['value'],
})

_subclass(IROperation, {
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
})

_subclass(IRProducingOp, {
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
	
	'GetModule': ['module'],	# type(module) = IRModule
	'MakeFunction': ['code', 'defaults', 'closures'],	# type(code) = IRFunction
	'MakeClass': ['name', 'superclasses'],
	
	#these are actually builtin functions, but they may be assigned to...
	'GetType': ['inspected'],		# type(inspected)
	'Iter': ['arg'],
	'Next': ['arg']
})
'''
_subclass(BinOp, op, []) for op in [
	'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Pow',
	'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd',
	
	'AugAdd', 'AugSub', 'AugMult', 'AugDiv', 'AugFloorDiv', 'AugMod', 'AugPow',
	'AugLShift', 'AugRShift', 'AugBitOr', 'AugBitXor', 'AugBitAnd',

	'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn',
	
	'And', 'Or'
]]

_subclass(UnaryOp, op, []) for op in [
	'Invert', 'Not', 'UAdd', 'USub'
]]
'''
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

_subclass(IREnvironment, {
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
})
