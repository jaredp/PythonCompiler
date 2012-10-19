
from time import clock

def fib(n):
	if n == 1:
		return 1
	elif n == 2:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)

def main():
    start = clock()
    sum = 0
    #for i in range(1, 35):
    #    sum += fib(i)
    i = 1
    while i < 35:
    	sum += fib(i)
    	i += 1
    end = clock()
    print sum, ', found in', end - start, 'seconds'

main()
