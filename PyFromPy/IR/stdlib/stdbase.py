from IR.ir import *
from IR.environments import *

class P3CFunction(IRFunction):
	def __init__(self, fname, pyname, *args):
		self.cname = fname
		self.pyname = pyname
		self.docstring = None
		self.args = list(args)

	def __call__(this, *args):
		return ConstCall(this, list(args))

	def __repr__(this):
		return this.cname
		

class BuiltinException(object):
	'''
	figuring this out would mean figuring out types in the IR
	We're not there yet
	'''
	def __init__(self, ename):
		self.ename = ename
		globals()[ename] = self

	def __repr__(self):
		return self.ename

modules = {}
def moduleNamed(mname):
	mod = IRModule(mname)
	modules[mname] = mod
	
	def BuiltinFn(pyname, cname, *args, **kwargs):
		fn = P3CFunction(cname, pyname, *args, **kwargs)
		fn.module = mname

		fnvar = IRVar(pyname)
		mod.namespace[pyname] = fnvar
		mod.initcode.body.append(
			MakeFunction(fnvar, fn, [], [])
		)

	def buildModule():
		# so the C function always returns something
		n = IRVar('none')
		mod.initcode.body.extend([
			NoneLiteral(n),
			Return(n)
		])
	
	return BuiltinFn, buildModule

