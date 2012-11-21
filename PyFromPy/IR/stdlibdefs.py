from IR.ir import *

class IRBuiltinFunction(IRFunction):
	body = None
	namespace = None
	isgenerator = False

	pyname = '`unnamedbuiltin`'
	varargs = []
	kwargs = []
	
	defaults = []
	captures = []
	globals = []
	
	def callOp(this, dest, *args):
		return ConstCall(dest, this, list(args))
	
	def callVoidOp(this, *args):
		return this.callOp(None, *args)
	
	def __repr__(this):
		return '<%s::%s>' % (this.cname, this.pyname)

PrintBuiltinTo = IRBuiltinFunction(
	cname = 'PyPrint',
	args = ['dest', 'obj']
)

PrintBuiltin = IRBuiltinFunction(
	cname = 'MyPrint',
	args = ['obj']
)

PrintNLBuiltin = IRBuiltinFunction(
	cname = 'PyPrintNl',
	args = []
)

