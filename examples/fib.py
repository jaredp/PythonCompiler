
import time

def fib(n):
	if n == 1:
		return 1
	elif n == 2:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)

def main():
    start = time.clock()
    sum = 0
    for i in range(1, 35):
        sum += fib(i)
    end = time.clock()
    print sum, ', found in', end - start, 'seconds'

main()
