
from time import clock as fclock

def fib(n):
	'''fib computes the nth number of the fibonacci sequence'''
	if n == 1:
		return 1
	elif n == 2:
		return 1
	else:
		''' base cases covered '''
		return fib(n - 1) + fib(n - 2)

def m():
	start = fclock()
	sum = 0
	#for i in range(1, 35):
	#    sum += fib(i)
	i = 1
	while i < 35:
		sum += fib(i)
		i += 1
	end = fclock()
	print sum, ', found in', end - start, 'seconds'
	
m()
