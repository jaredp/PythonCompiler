from CTranslator import CTranslator
import sys

def generateProgram(program, out=sys.stdout, ints_only=False):
	t = (CTranslator if not ints_only else IntOnlyCTranslator)
	translator = t(out)
	translator.generateProgram(program)
	
class IntOnlyCTranslator(CTranslator):
	def writeHeader(self):
		self.write('#include <P3IntsLib.h>'); self.fill()
		
	def generateFnPosCaller(self, fn):
		pass
	
	def fdeclaration(self, function):
		args = ', '.join(map(self.declaration, function.argvars))
		return 'int %s(%s)' % (function.cname, args)

	def declaration(self, varname):
		return 'int %s' % varname
		
	def declare(self, varname):
		self.fill('%s = 0;' % self.declaration(varname))
