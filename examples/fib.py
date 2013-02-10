#from __builtin__ import raw_input, int
from time import clock as fclock

def fib(n):
	'''fib computes the nth number of the fibonacci sequence'''
	if n == 1:
		return 1
	elif n == 2:
		return 1

	return fib(n - 1) + fib(n - 2)

def m(maxfib):
	start = fclock()
	sum = 0
	#for i in range(1, 35):
	#    sum += fib(i)
	i = 1
	while i < maxfib:
		sum += fib(i)
		i += 1
	end = fclock()
	print sum, ', found in', end - start, 'seconds'

#maxfib = int(raw_input('sum fib to '))	
m(35)#(maxfib)
