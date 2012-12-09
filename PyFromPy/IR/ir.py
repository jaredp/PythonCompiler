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
	'IROperation': [],	
	'IRBlockStatement': [],
 })

# all code blocks are non-None [IROperation|IRBlockStatement]

_subclass(IRBlockStatement, {
	'If': ['condition', 'then', 'orelse'],	# condition is an IRVar
	'Loop': ['body'],
	'Try': ['body', 'exception', 'handler']
	# type(exception) = None|BuiltinException|IRVar
})

_subclass(IROperation, {
	# majority of OPs are IRProducingOps, meaning they produce something
	# IRProducing OPs are intended to be like 3-address code
	'IRProducingOp': ['target'],	# type(target) = IRVar|None
	
	'Return': ['value'],
	'Yield': ['value'],
	'Raise': ['exception'],			# type(exception) = IRVar|IRExceptionBuiltin|None
	
	'Break': [],
	'Continue': [],

	'DeleteVar': ['var'],
	'AssignAttr': ['obj', 'attr', 'value'],	
	'DeleteAttr': ['obj', 'attr'],
})

_subclass(IRProducingOp, {
	# type(fn) = IRVar; type(kwargs) = (pyname, IRVar)
	'FCall': ['fn', 'args', 'kwargs', 'starargs', 'keystarargs'],
	'MethodCall': ['object', 'methname', 'args', 'kwargs', 'starargs', 'keystarargs'],

	# type(fn) = IRFunction
	'ConstCall': ['fn', 'args'],
	
	'Assign': ['rhs'],
	'Attr':	['obj', 'attr'],
	# add mechanism for direct access
	
	'IRStringLiteral': ['value'],
	'IRIntLiteral': ['value'],
	'IRFloatLiteral': ['value'],
	'NoneLiteral': [],

	'GetModule': ['module'],	# used for imports; type(module) = IRModule
	'MakeFunction': ['code', 'defaults', 'closures'],	# type(code) = IRFunction
	'MakeClass': ['klass'],		# type(klass) = IRClass

	# context dependant
	'GetGeneratorSentIn': [],	# target = yield
	'GetException': [],			# except Exception as target: ...; none if no exception

	# these may be removed
	'GetLocals': [],			# locals(), but locals can be assigned
	'GetGlobals': [],			# globals(), but globals can be assigned
})

