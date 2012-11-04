def a():
	a = 4
	def q():
		print a
		print b
	locals()['b'] = 4
	print locals()
	print a
	print b
	q()

a()
b
	
	
