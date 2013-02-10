from IR import *
from base import *
from utils import escapeString

def _IRIntLiteral(var):
	return "P3IntLiteral(%s)" % var.value

def _IRFloatLiteral(var):
	return "P3FloatLiteral(%s)" % var.value

def _IRStringLiteral(var):
	return 'P3StringLiteral("%s")' % escapeString(var.value)

def _NoneLiteral(var):
	return 'Py_None'

def _If(irexpr):
	#TODO
	fill('if (isTruthy(%s))' % irexpr.condition)
	genBlock(irexpr.then)
	if irexpr.orelse:
		write('else')
		genBlock(irexpr.orelse)

def _Loop(irexpr):
	fill('while (1)')
	genBlock(irexpr.body)

def _Return(irexpr):
	return "return %s" % irexpr.value

def _Break(irexpr):
	return "break"

def _Continue(irexpr):
	return "continue"

def _AssignAttr(op):
	return (
		'P3AssignAttr(%s, "%s", %s)' % 
		(op.obj, escapeString(op.attr), op.value)
	)

def _Attr(op):
	return 'P3GetAttr(%s, "%s")' % (op.obj, escapeString(op.attr))

def _DeleteAttr(op):
	return 'P3DelAttr(%s, %s)' % (op.obj, obj.attr)

def _DeleteVar(irexpr):
	'''
	Delete is the Python `del`, which unbinds a name.
	For now, according to the CPython C-API, the python del 
	statement translates to lowering the refcount and setting the
	variable to NULL.
	This actually raises a whole host of ugly questions about how
	to identify and handle unbound names.
	The most obvious solution is to precede all operations with a
	null-check on their operands, but this is ham-fisted as there
	are ways to show which (many) are unnecessary.
	Furthermore, the del statement is pretty rare in python code
	anyway.
	'''
	return 'Py_DECREF(%s); %s = NULL' % (irexpr.var, irexpr.var)

def _FCall(fcall):
	'''
	The function calling mechanism will be among the most
	complex, and in some ways are the focus of this 
	research.  C certainly doesn't have the type of variable
	argument function calling mechanism Python does, so this
	is not a straightforward translation.
	For now, we're going to just call the _ConstCall mechanism.
	'''
	if fcall.starargs != None \
	or fcall.keystarargs != None \
	or fcall.kwargs != []: 
		raise NotImplementedError

	else:
		argcount = len(fcall.args)
		arglist = ' '.join([
			'PyTuple_SET_ITEM(args, %s, %s);' % a
			for a in zip(range(argcount), fcall.args)
		])
		return (
			'P3Call(%s, ({PyObject *args = PyTuple_New(%s);%s args;}))'
			% (fcall.fn, argcount, arglist)
		)

def _MethodCall(irexpr):
	'''
	This is the _FCall mechanism, with all the added fun of
	class attribute lookup.  It's entirely possible we wont
	get to classes, and not get to this.
	'''
	raise NotImplementedError

def _ConstCall(irexpr):
	args = ', '.join(map(repr, irexpr.args))
	return '%s(%s)' % (irexpr.fn, args)

def _Assign(irexpr):
	return repr(irexpr.rhs)

#Take IRClass/IRFunction/IRModule and turn them into py objects:
def _MakeFunction(op):
	return (
		'P3MakeFunction((fptr)%s_POSCALLER, "%s")'
		% (op.code.cname, op.code.pyname)
	)

def _MakeClass(op):
	'''
	These properly should be structs defined at top-level
	Same for modules.
	This should just get them.
	For now, we're actually going to make them with the
	fallback usually reserved for type(,,)
	'''
	return 'P3MakeClass("%s")' % op.klass.name

def _GetModule(op):
	return op.module.cname

# exception handling
def _Try(irexpr):
	raise NotImplementedError

def _Raise(irexpr):
	raise NotImplementedError

def _GetException(irexpr):
	raise 'P3GetException()'

# generator handling
def _Yield(irexpr):
	'''
	Generators are considerably complicated,
	and require tricky C generation support.
	Yield is not a keyword in C/C++
	'''
	raise NotImplementedError

def _GetGeneratorSentIn(irexpr):
	raise NotImplementedError



