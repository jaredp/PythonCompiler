'''
a, b = (4, 5)
print a

a = 4.45 + 6
b = 'Hello' + 'world!'
for i in (a, b):
	print i
'''

def range(i, n):
	r = []
	while i < n:
		r += [i]
		i += 1
	return r

def fib(n):
	'''fib computes the nth number of the fibonacci sequence'''
	if n == 1:
		return 1
	elif n == 2:
		return 1
	else:
		''' base cases covered '''
		return fib(n - 1) + fib(n - 2)

sum = 0
for i in range(1, 35):
	sum += fib(i)

print sum
