class C(object):
	def __add__(self, rhs):
		print "not in place"
		return self

	def __iadd__(self, rhs):
		print "in place"
		return self

a = C()
b = C()

c = a + b
a = a + b
d = a
a += b

