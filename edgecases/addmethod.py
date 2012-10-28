
def fn(self, n):
	self.n += n
	
class C(object):
	pass
	
C.meth = fn

obj = C()
obj.n = 2
obj.meth(5)

print obj.n
