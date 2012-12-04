'''
a, b = (4, 5)
print a

a = 4.45 + 6
b = 'Hello' + 'world!'
for i in (a, b):
	print i
'''

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
i = 1
while i < 35:
	sum += fib(i)
	i += 1

print sum
