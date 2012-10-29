class A(object):
	def getcolor(self):
		return 'blue'
	color = property(getcolor)
	def fmt(self):
		return self.color + ': ' + self.text

class A1(A):
	def getcolor(self):
		self._color = 'green'
		return self._color
	color = property(getcolor)

class A2(A):
	def fmt(self):
		return self.text

o = A()
o.text = 'foobar'
print o.fmt(), o.__dict__

o.__class__ = A1
print o.fmt(), o.__dict__

o.__class__ = A2
print o.fmt(), o.__dict__

