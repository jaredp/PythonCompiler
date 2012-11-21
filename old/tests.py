from astutils import *
from utils import *

a = Name('x', Assign())
b = None

def perSubexprTest():
	def t(node, block):
		if node == a:
			return b
		else:
			return node
	e = BinOp(a, Add(), a)
	stmts = []
	
	log(e)
	e = perSubexpr(t, e, stmts)
	log(e)

def perExprTest():
	@perExpr
	def t(node, block):
		if node == a:
			return b
		else:
			return node

	stmt = Assign([a], a)
	stmts = mkVanillaFunction('f', [], [stmt])

	log(stmts)
	t(stmts)
	log(stmts)

if __name__ == '__main__':
	perSubexprTest()
	perExprTest()
