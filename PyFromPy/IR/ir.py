
from IR.base import IRNode, _IRVar

def _subclass(superclass, subclasses):
	bases = (superclass,)
	for name, components in subclasses.items():
		newclass = type(name, bases, {'__slots__':components})
		globals()[name] = newclass


#############################################################
# IRNodes
#############################################################

_subclass(IRNode, {
	'IRAtom': [],		# argument to operation
	'IROperation': [],	
	'IRBlock': [],
 })

# all code blocks are non-None [IROperation|IRBlock]

_subclass(IRBlock, {
	'If': ['condition', 'then', 'orelse'],	# condition is an IRAtom
	'While': ['condition', 'body'],
	'Try': ['body', 'catch', 'finally']
	# type(catch) = None|(exception (pyname), as (pyname), handler (code block))
})

_subclass(IRAtom, {
	'IRStringLiteral': ['value'],
	'IRIntLiteral': ['value'],
	'IRFloatLiteral': ['value'],
	'NoneLiteral': []
})
class IRVar(IRAtom, _IRVar): pass

_subclass(IROperation, {
	# majority of OPs are IRProducingOps, meaning they produce something
	# IRProducing OPs are intended to be like 3-address code
	'IRProducingOp': ['target'],	# type(target) = IRVar|None
	
	'Return': ['value'],
	'Yield': ['value'],
	'Raise': ['exception'],
		
	'AssignAttr': ['obj', 'attr', 'value'],
	'AssignSubscript': ['obj', 'subscript', 'value'],
	'AssignSlice': ['obj', 'start', 'end', 'step', 'value'],
	# start, end, and step can be None
	
	'DeleteVar': ['var'],			# IRVar
	'DeleteAttr': ['obj', 'attr'],

	'DeleteSubscript': ['obj', 'subscript'],
	'DeleteSlice': ['obj', 'start', 'end', 'step'],
})

_subclass(IRProducingOp, {
	'BinOp': ['lhs', 'rhs'],
	'UnaryOp': ['arg'],

	# type(fn) = IRAtom
	'FCall': ['fn', 'args', 'kwargs', 'starargs', 'keystarargs'],
	'MethodCall': ['object', 'methname', 'args', 'kwargs', 'starargs', 'keystarargs'],

	# type(fn) = IRFunction
	'ConstCall': ['fn', 'args'],
	
	'Assign': ['rhs'],
	'Attr':	['obj', 'attr'],
	'Subscript': ['obj', 'subscript'],
	'Slice': ['obj', 'start', 'end', 'step'],
	
	# context dependant
	'GetGeneratorSentIn': [],	# x = yield
	'GetLocals': [],			# locals(), but locals can be assigned
	'GetGlobals': [],			# globals(), but globals can be assigned
	
	'GetModule': ['module'],	# used for imports; type(module) = IRModule
	'MakeFunction': ['code', 'defaults', 'closures'],	# type(code) = IRFunction
	'MakeClass': ['name', 'superclasses']
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

