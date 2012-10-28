
all : out/cfib

out/fib.cpp : *.py pylib/*
	./py++ ../examples/fib.py > out/fib.cpp

out/cfib : out/fib.cpp
	g++ out/fib.cpp pylib/*.cpp -O3 -o out/cfib

.PHONY : run
run : out/cfib
	out/cfib

.PHONY : clean
clean :
	rm out/*
